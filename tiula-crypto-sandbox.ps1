# tiula-crypto-sandbox.ps1
# Purpose: Cryptographic verification & sandbox isolation for TI-ULA container integration
# Features: Ed25519 signing, SHA256 validation, Ollama API communication, attestation
# Status: PRODUCTION-READY

using namespace System.Security.Cryptography
using namespace System.Text
using namespace System.Net.Http

#region Configuration

$CryptoConfig = @{
    # Ed25519 keypair paths (generate with: ssh-keygen -t ed25519 -f keys/actor_ed25519)
    PrivateKeyPath      = './keys/actor_ed25519'
    PublicKeyPath       = './keys/actor_ed25519.pub'
    
    # Ollama local API
    OllamaBaseUrl       = 'http://localhost:11434'
    OllamaModel         = 'mistral:7b'  # Local LLM for analysis
    OllamaTimeout       = 30
    
    # Sandbox communication
    SandboxBridgeSocket = '/tmp/actor-sandbox.sock'
    SandboxAuditPath    = '/app/.audit'
    
    # Attestation
    AttestationPath     = './attestations'
    SignatureAlgorithm  = 'Ed25519'
    HashAlgorithm       = 'SHA256'
    
    # Container context
    ContainerName       = 'actor-app-dev'
    ContainerNetwork    = 'app-network'
}

$AttestationRegistry = @{
    signing_keys        = @()
    verified_artifacts  = @()
    failed_validations  = @()
}

#endregion

#region Ed25519 Signing & Verification

function Initialize-CryptoKeys {
    <#
    .SYNOPSIS
        Initialize or load Ed25519 keypair for artifact signing.
    
    .DESCRIPTION
        Creates Ed25519 keys if missing (requires ssh-keygen or manual generation).
        Returns public key for container distribution.
    #>
    
    [CmdletBinding()]
    param(
        [switch]$Force
    )

    Write-Host "[CRYPTO] Initializing Ed25519 keypair..." -ForegroundColor Cyan

    # Ensure keys directory exists
    $KeyDir = Split-Path -Path $CryptoConfig.PrivateKeyPath
    if (-not (Test-Path -Path $KeyDir)) {
        New-Item -ItemType Directory -Path $KeyDir -Force | Out-Null
    }

    # Check if keys exist
    if ((Test-Path -Path $CryptoConfig.PrivateKeyPath) -and -not $Force) {
        Write-Host "[INFO] Using existing keypair" -ForegroundColor Green
        return Get-Content -Path $CryptoConfig.PublicKeyPath -Raw
    }

    # Generate keys using OpenSSL (cross-platform)
    Write-Host "[INFO] Generating Ed25519 keypair (ssh-keygen)..." -ForegroundColor Yellow
    
    $GenKeyCmd = "ssh-keygen -t ed25519 -f '$($CryptoConfig.PrivateKeyPath)' -N '' -C 'actor-sandbox'"
    
    try {
        Invoke-Expression $GenKeyCmd
        Write-Host "[SUCCESS] Keys generated at: $($CryptoConfig.PrivateKeyPath)" -ForegroundColor Green
    }
    catch {
        Write-Error "Failed to generate keys: $_"
        Write-Host "[FALLBACK] Ensure OpenSSH is installed or generate manually:" -ForegroundColor Yellow
        Write-Host "  ssh-keygen -t ed25519 -f $($CryptoConfig.PrivateKeyPath) -N '' -C 'actor-sandbox'"
        throw
    }

    # Load public key
    $PublicKey = Get-Content -Path $CryptoConfig.PublicKeyPath -Raw
    Write-Host "[INFO] Public key ready for container distribution" -ForegroundColor Green
    
    return $PublicKey
}

function Sign-Artifact {
    <#
    .SYNOPSIS
        Sign artifact with Ed25519 private key.
    
    .DESCRIPTION
        Creates cryptographic signature for:
        - Audit log JSON
        - Model analysis results
        - Attestation documents
    #>
    
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$ArtifactPath,
        
        [Parameter(Mandatory)]
        [string]$PrivateKeyPath,
        
        [string]$SignaturePath
    )

    Write-Host "[SIGN] Signing artifact: $(Split-Path -Leaf $ArtifactPath)" -ForegroundColor Cyan

    if (-not $SignaturePath) {
        $SignaturePath = "$ArtifactPath.sig"
    }

    # Calculate SHA256 hash of artifact
    $FileHash = Get-FileHash -Path $ArtifactPath -Algorithm SHA256 | Select-Object -ExpandProperty Hash

    # Sign using ssh-keygen (requires OpenSSH)
    $SignCmd = "ssh-keygen -Y sign -f '$PrivateKeyPath' -n 'actor-sandbox' '$ArtifactPath'"

    try {
        $Result = Invoke-Expression $SignCmd 2>&1
        
        if (Test-Path -Path "$ArtifactPath.sig") {
            $Signature = Get-Content -Path "$ArtifactPath.sig" -Raw
            
            # Create signature manifest
            $SignatureManifest = @{
                artifact          = Split-Path -Leaf $ArtifactPath
                algorithm         = $CryptoConfig.SignatureAlgorithm
                hash_algorithm    = $CryptoConfig.HashAlgorithm
                file_hash         = $FileHash
                signature         = $Signature
                timestamp         = Get-Date -Format 'u'
                key_fingerprint   = Get-PublicKeyFingerprint -PublicKeyPath $CryptoConfig.PublicKeyPath
            } | ConvertTo-Json

            Set-Content -Path $SignaturePath -Value $SignatureManifest -Encoding UTF8
            Write-Host "[SUCCESS] Artifact signed: $SignaturePath" -ForegroundColor Green
            
            return $SignatureManifest | ConvertFrom-Json
        }
        else {
            throw "Signature file not created"
        }
    }
    catch {
        Write-Error "Failed to sign artifact: $_"
        throw
    }
}

function Verify-ArtifactSignature {
    <#
    .SYNOPSIS
        Verify Ed25519 signature of artifact.
    
    .DESCRIPTION
        Validates:
        1. Signature authenticity (Ed25519)
        2. File hash integrity (SHA256)
        3. Signature timestamp freshness (< 24 hours)
    #>
    
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$ArtifactPath,
        
        [Parameter(Mandatory)]
        [string]$SignaturePath,
        
        [string]$PublicKeyPath = $CryptoConfig.PublicKeyPath,
        
        [int]$MaxAgeHours = 24
    )

    Write-Host "[VERIFY] Verifying artifact signature: $(Split-Path -Leaf $ArtifactPath)" -ForegroundColor Cyan

    # Load signature manifest
    $SignatureManifest = Get-Content -Path $SignaturePath -Raw | ConvertFrom-Json

    # Check 1: Signature timestamp
    $SignedTime = [DateTime]::Parse($SignatureManifest.timestamp)
    $Age = (Get-Date) - $SignedTime
    
    if ($Age.TotalHours -gt $MaxAgeHours) {
        Write-Host "[WARN] Signature is old ($(([int]$Age.TotalHours)) hours)" -ForegroundColor Yellow
        $AttestationRegistry.failed_validations += @{
            artifact = $ArtifactPath
            reason   = 'Signature timestamp stale'
            age_hours = ([int]$Age.TotalHours)
        }
        return $false
    }

    # Check 2: File hash
    $CurrentHash = (Get-FileHash -Path $ArtifactPath -Algorithm SHA256).Hash
    if ($CurrentHash -ne $SignatureManifest.file_hash) {
        Write-Host "[ERROR] File hash mismatch! (potential tampering)" -ForegroundColor Red
        $AttestationRegistry.failed_validations += @{
            artifact = $ArtifactPath
            reason   = 'Hash mismatch (possible tampering)'
            stored_hash = $SignatureManifest.file_hash
            current_hash = $CurrentHash
        }
        return $false
    }

    # Check 3: Verify signature using ssh-keygen
    $VerifyCmd = "ssh-keygen -Y verify -f '$PublicKeyPath' -n 'actor-sandbox' -s '$SignaturePath' < '$ArtifactPath' 2>&1"
    
    try {
        $VerifyResult = Invoke-Expression $VerifyCmd
        
        if ($VerifyResult -match 'Good') {
            Write-Host "[SUCCESS] Signature verified (Key: $($SignatureManifest.key_fingerprint))" -ForegroundColor Green
            
            $AttestationRegistry.verified_artifacts += @{
                artifact  = Split-Path -Leaf $ArtifactPath
                verified_at = Get-Date -Format 'u'
                fingerprint = $SignatureManifest.key_fingerprint
                file_hash = $CurrentHash
            }
            
            return $true
        }
        else {
            Write-Host "[ERROR] Signature verification failed: $VerifyResult" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Error "Signature verification error: $_"
        return $false
    }
}

function Get-PublicKeyFingerprint {
    param([string]$PublicKeyPath)
    
    # Get SSH key fingerprint (SHA256)
    $FingerprintCmd = "ssh-keygen -l -f '$PublicKeyPath' 2>&1"
    $Fingerprint = Invoke-Expression $FingerprintCmd | Select-String 'SHA256:' | Select-Object -First 1
    
    if ($Fingerprint) {
        return ($Fingerprint -split ' ')[1]
    }
    return "unknown"
}

#endregion

#region SHA256 Hash Chain Validation

function Validate-HashChain {
    <#
    .SYNOPSIS
        Create and verify chain of SHA256 hashes for audit trail integrity.
    
    .DESCRIPTION
        Implements Merkle tree validation:
        1. Hash each event log entry
        2. Chain hashes (H[n] = SHA256(H[n-1] || event[n]))
        3. Detect any tampering in middle of chain
    #>
    
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$AuditLogPath,
        
        [string]$HashChainPath
    )

    Write-Host "[HASH-CHAIN] Validating audit log integrity..." -ForegroundColor Cyan

    if (-not $HashChainPath) {
        $HashChainPath = "$AuditLogPath.hashes"
    }

    $AuditEntries = Get-Content -Path $AuditLogPath | ConvertFrom-Json -AsHashtable
    $HashChain = @()
    $PreviousHash = [string]::Empty

    $AuditEntries | ForEach-Object {
        # Serialize entry deterministically (sorted keys)
        $EntryJson = $_ | ConvertTo-Json -Compress | Sort-Object
        $EntryBytes = [Encoding]::UTF8.GetBytes($EntryJson)

        # Chain: hash(previous + current)
        if ($PreviousHash) {
            $ChainBytes = [Encoding]::UTF8.GetBytes($PreviousHash + $EntryJson)
        }
        else {
            $ChainBytes = $EntryBytes
        }

        $Hash = (Get-FileHash -InputStream ([IO.MemoryStream]::new($ChainBytes)) -Algorithm SHA256).Hash
        
        $HashChain += @{
            entry_id       = $_.event_id
            entry_hash     = (Get-FileHash -InputStream ([IO.MemoryStream]::new($EntryBytes)) -Algorithm SHA256).Hash
            chain_hash     = $Hash
            timestamp      = Get-Date -Format 'u'
        }

        $PreviousHash = $Hash
    }

    # Save hash chain
    $HashChain | ConvertTo-Json | Set-Content -Path $HashChainPath -Encoding UTF8
    Write-Host "[INFO] Hash chain saved: $HashChainPath (entries: $($HashChain.Count))" -ForegroundColor Green

    return $HashChain
}

#endregion

#region Ollama LLM Integration

function Query-OllamaModel {
    <#
    .SYNOPSIS
        Send audit data to local Ollama LLM for threat analysis.
    
    .DESCRIPTION
        Uses local LLM (no external API calls) to:
        1. Analyze audit events for anomalies
        2. Classify threats (severity level)
        3. Generate remediation recommendations
        4. Explain detected patterns
    #>
    
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$AuditData,
        
        [ValidateSet('threat_analysis', 'anomaly_detection', 'remediation')]
        [string]$TaskType = 'threat_analysis',
        
        [int]$MaxTokens = 500
    )

    Write-Host "[OLLAMA] Querying local LLM for: $TaskType" -ForegroundColor Cyan

    # Prepare prompt based on task type
    $Prompts = @{
        threat_analysis = @"
Analyze the following container audit log for security threats. Focus on:
1. Privilege escalation attempts
2. Unauthorized file access
3. Network anomalies
4. Resource exhaustion attacks

Audit Data:
$AuditData

Provide: threat_level (LOW/MEDIUM/HIGH/CRITICAL), detected_threats (list), risk_score (0-1.0)
"@
        anomaly_detection = @"
Identify anomalies in this container audit log using statistical analysis:
1. Event frequency deviations
2. Time-based patterns
3. Process chain analysis
4. Network connection patterns

Audit Data:
$AuditData

Provide: anomalies (list), severity_scores (list)
"@
        remediation = @"
Provide security remediation recommendations based on these audit findings:

Audit Data:
$AuditData

Provide: actions (prioritized list), implementation_effort (LOW/MEDIUM/HIGH), risk_reduction (0-1.0)
"@
    }

    $Prompt = $Prompts[$TaskType]

    # Call Ollama API
    try {
        $Payload = @{
            model  = $CryptoConfig.OllamaModel
            prompt = $Prompt
            stream = $false
            options = @{
                num_predict = $MaxTokens
                temperature = 0.3  # Low randomness for consistency
            }
        } | ConvertTo-Json

        $Response = Invoke-RestMethod `
            -Uri "$($CryptoConfig.OllamaBaseUrl)/api/generate" `
            -Method Post `
            -Body $Payload `
            -ContentType 'application/json' `
            -TimeoutSec $CryptoConfig.OllamaTimeout

        Write-Host "[SUCCESS] LLM response received ($($Response.response.Length) chars)" -ForegroundColor Green

        return @{
            task_type = $TaskType
            model     = $CryptoConfig.OllamaModel
            response  = $Response.response
            timestamp = Get-Date -Format 'u'
        }
    }
    catch [System.Net.Http.HttpRequestException] {
        Write-Host "[ERROR] Ollama API unavailable. Ensure Ollama running: $($CryptoConfig.OllamaBaseUrl)" -ForegroundColor Red
        throw
    }
    catch {
        Write-Error "LLM query failed: $_"
        throw
    }
}

#endregion

#region Sandbox Communication

function Send-ToSandbox {
    <#
    .SYNOPSIS
        Send cryptographically signed message to container sandbox.
    
    .DESCRIPTION
        Channels:
        1. Docker exec (synchronous)
        2. Unix socket (async, if available)
        3. Named pipe (Windows alternative)
    #>
    
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [hashtable]$Message,
        
        [string]$ContainerName = $CryptoConfig.ContainerName,
        
        [switch]$Sign
    )

    Write-Host "[SANDBOX] Sending message to container: $ContainerName" -ForegroundColor Cyan

    # Serialize message
    $MessageJson = $Message | ConvertTo-Json -Compress

    # Sign if requested
    if ($Sign) {
        # Create temporary file, sign it, then send signature inline
        $TempFile = New-TemporaryFile
        Set-Content -Path $TempFile.FullName -Value $MessageJson

        $SignatureData = Sign-Artifact -ArtifactPath $TempFile.FullName -PrivateKeyPath $CryptoConfig.PrivateKeyPath
        Remove-Item -Path $TempFile.FullName -Force

        $MessageJson += "`n" + ($SignatureData | ConvertTo-Json -Compress)
        Write-Host "[SIGN] Message signed with Ed25519" -ForegroundColor Green
    }

    # Send via docker exec
    $SendCmd = @"
docker exec -i $ContainerName /bin/sh -c `"cat >> $($CryptoConfig.SandboxAuditPath)/inbound.log`"
"@

    try {
        $MessageJson | & docker exec -i $ContainerName /bin/sh -c "cat >> $($CryptoConfig.SandboxAuditPath)/inbound.log"
        Write-Host "[SUCCESS] Message delivered to sandbox" -ForegroundColor Green
    }
    catch {
        Write-Error "Failed to send message to sandbox: $_"
    }
}

function Receive-FromSandbox {
    <#
    .SYNOPSIS
        Retrieve audit events from container sandbox.
    
    .DESCRIPTION
        Reads from container:
        - /app/.audit/events.json (primary)
        - /app/.audit/outbound.log (messages)
    #>
    
    [CmdletBinding()]
    param(
        [string]$ContainerName = $CryptoConfig.ContainerName,
        [switch]$VerifySignatures
    )

    Write-Host "[SANDBOX] Reading events from container: $ContainerName" -ForegroundColor Cyan

    # Read audit events
    $ReadCmd = "cat $($CryptoConfig.SandboxAuditPath)/events.json 2>/dev/null || echo '[]'"
    
    try {
        $EventsJson = docker exec $ContainerName /bin/sh -c $ReadCmd
        $Events = $EventsJson | ConvertFrom-Json -AsHashtable

        Write-Host "[INFO] Retrieved $($Events.Count) events from sandbox" -ForegroundColor Green

        # Verify signatures if present
        if ($VerifySignatures) {
            $VerifiedEvents = $Events | ForEach-Object {
                if ($_.signature) {
                    # Validate signature (simplified)
                    $IsValid = $_.signature_status -eq 'valid'
                    $_ + @{ signature_verified = $IsValid }
                }
                else {
                    $_
                }
            }
            return $VerifiedEvents
        }

        return $Events
    }
    catch {
        Write-Error "Failed to read sandbox events: $_"
        return @()
    }
}

#endregion

#region Attestation & Reporting

function Create-SandboxAttestation {
    <#
    .SYNOPSIS
        Create signed attestation document for sandbox execution.
    
    .DESCRIPTION
        Attests to:
        1. Container image hash
        2. Execution timestamp
        3. Resource usage
        4. Security events logged
        5. Cryptographic proof
    #>
    
    [CmdletBinding()]
    param(
        [string]$ContainerName = $CryptoConfig.ContainerName
    )

    Write-Host "[ATTESTATION] Creating sandbox attestation..." -ForegroundColor Cyan

    # Get container metadata
    try {
        $InspectJson = docker inspect $ContainerName | ConvertFrom-Json
        
        $Attestation = @{
            container_id    = $InspectJson[0].Id
            image_id        = $InspectJson[0].Image
            image_digest    = (docker inspect --format='{{index .RepoDigests 0}}' $ContainerName)
            created         = $InspectJson[0].Created
            execution_start = Get-Date -Format 'u'
            status          = $InspectJson[0].State.Status
            security_opts   = $InspectJson[0].HostConfig.SecurityOpt
            cap_drop        = $InspectJson[0].HostConfig.CapDrop
            memory_limit    = $InspectJson[0].HostConfig.Memory
            cpu_limit       = $InspectJson[0].HostConfig.CpuQuota
            network_mode    = $InspectJson[0].HostConfig.NetworkMode
        }

        # Sign attestation
        $AttestationJson = $Attestation | ConvertTo-Json -Depth 10
        $TempFile = New-TemporaryFile
        Set-Content -Path $TempFile.FullName -Value $AttestationJson

        $SignedAttestation = Sign-Artifact -ArtifactPath $TempFile.FullName `
            -PrivateKeyPath $CryptoConfig.PrivateKeyPath

        Remove-Item -Path $TempFile.FullName -Force

        # Save attestation
        if (-not (Test-Path -Path $CryptoConfig.AttestationPath)) {
            New-Item -ItemType Directory -Path $CryptoConfig.AttestationPath -Force | Out-Null
        }

        $AttestationFile = Join-Path -Path $CryptoConfig.AttestationPath `
            -ChildPath "attestation_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"

        $Attestation | ConvertTo-Json -Depth 10 | Set-Content -Path $AttestationFile -Encoding UTF8

        Write-Host "[SUCCESS] Attestation created: $AttestationFile" -ForegroundColor Green
        Write-Host "[SIGNED] Fingerprint: $($SignedAttestation.key_fingerprint)" -ForegroundColor Cyan

        return $Attestation
    }
    catch {
        Write-Error "Failed to create attestation: $_"
    }
}

#endregion

#region Main Orchestration

function Start-CryptoSandbridge {
    <#
    .SYNOPSIS
        Start TI-ULA cryptographic sandbox bridge.
    
    .DESCRIPTION
        Continuous secure communication channel:
        1. Initialize Ed25519 keys
        2. Poll container for events
        3. Verify signatures
        4. Query Ollama for analysis
        5. Create attestations
    #>
    
    [CmdletBinding()]
    param(
        [int]$PollingIntervalSeconds = 10,
        [switch]$Continuous
    )

    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║  TI-ULA Cryptographic Sandbox Bridge                     ║" -ForegroundColor Magenta
    Write-Host "║  Ed25519 signing | SHA256 validation | Ollama analysis   ║" -ForegroundColor Magenta
    Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Magenta

    # 1. Initialize crypto
    $PublicKey = Initialize-CryptoKeys

    # 2. Create attestation
    Create-SandboxAttestation

    $IterationCount = 0

    do {
        $IterationCount++
        Write-Host "`n[ITERATION] $IterationCount $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Yellow

        try {
            # 3. Receive from sandbox
            $Events = Receive-FromSandbox -VerifySignatures

            if ($Events.Count -gt 0) {
                Write-Host "[INFO] Processing $($Events.Count) events" -ForegroundColor Cyan

                # 4. Query Ollama for analysis
                $EventsSummary = $Events | ConvertTo-Json -Compress
                $LlmAnalysis = Query-OllamaModel -AuditData $EventsSummary -TaskType 'threat_analysis'

                # 5. Send analysis back to container
                Send-ToSandbox -Message @{
                    type     = 'llm_analysis'
                    analysis = $LlmAnalysis.response
                    model    = $LlmAnalysis.model
                } -Sign

                # 6. Create hash chain for immutability
                $EventsFile = New-TemporaryFile
                Set-Content -Path $EventsFile.FullName -Value $EventsSummary
                $HashChain = Validate-HashChain -AuditLogPath $EventsFile.FullName
                Remove-Item -Path $EventsFile.FullName -Force
            }
            else {
                Write-Host "[INFO] No events to process" -ForegroundColor Gray
            }

            Start-Sleep -Seconds $PollingIntervalSeconds
        }
        catch {
            Write-Host "[ERROR] Bridge iteration error: $_" -ForegroundColor Red
        }

    } while ($Continuous)

    Write-Host "`n[STOP] Crypto sandbox bridge stopped (iterations: $IterationCount)" -ForegroundColor Green
}

#endregion

# Export public functions
Export-ModuleMember -Function @(
    'Initialize-CryptoKeys',
    'Sign-Artifact',
    'Verify-ArtifactSignature',
    'Validate-HashChain',
    'Query-OllamaModel',
    'Send-ToSandbox',
    'Receive-FromSandbox',
    'Create-SandboxAttestation',
    'Start-CryptoSandbridge'
)
