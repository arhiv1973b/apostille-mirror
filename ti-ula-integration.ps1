# ti-ula-integration.ps1 - TI-ULA Container ↔ Host Audit Bridge
# Purpose: Secure bidirectional communication between Docker container audits and host TI-ULA models
# Status: FUNCTIONAL | Requires: Docker CLI, jq (JSON parsing)

using namespace System.Net.Http
using namespace System.Text.Json

#region Configuration

$Config = @{
    ContainerName     = 'actor-app-dev'
    HostAuditPath     = "H:\ACTOR_DEV_ENV\audits"
    ContainerAuditPath = '/app/.audit'
    TiUlaModelPath    = "H:\ACTOR_DEV_ENV\models"
    LogLevel          = 'INFO'  # DEBUG, INFO, WARN, ERROR
    EnableCrypto      = $true   # Encrypt audit payloads at rest
}

$AuditEventTypes = @{
    CONTAINER_START    = 'container.start'
    CONTAINER_EXEC     = 'container.exec'
    FILE_ACCESS        = 'file.access'
    NETWORK_CONN       = 'network.connection'
    CAPABILITY_REQ     = 'capability.request'
    RESOURCE_USAGE     = 'resource.usage'
    ANOMALY_DETECTED   = 'anomaly.detected'
}

#endregion

#region Logging

function Write-AuditLog {
    [CmdletBinding()]
    param(
        [ValidateSet('DEBUG', 'INFO', 'WARN', 'ERROR')]
        [string]$Level = 'INFO',
        [Parameter(Mandatory)]
        [string]$Message,
        [hashtable]$Context
    )

    $Severity = @{ DEBUG = 0; INFO = 1; WARN = 2; ERROR = 3 }
    $LogLevelInt = @{ DEBUG = 0; INFO = 1; WARN = 2; ERROR = 3 }[$Config.LogLevel]
    
    if ($Severity[$Level] -lt $LogLevelInt) { return }

    $Timestamp = Get-Date -Format 'yyyy-MM-ddTHH:mm:ss.fffZ'
    $LogEntry = @{
        timestamp = $Timestamp
        level     = $Level
        message   = $Message
        context   = $Context
        hostname  = [System.Net.Dns]::GetHostName()
        pid       = $PID
    }

    $JsonLog = $LogEntry | ConvertTo-Json -Compress
    Write-Host "[$Level] $JsonLog"

    # Persist to audit log
    $AuditLog = Join-Path -Path $Config.HostAuditPath -ChildPath "ti-ula-bridge.log"
    Add-Content -Path $AuditLog -Value $JsonLog
}

#endregion

#region Container Communication

function Get-ContainerAuditEvents {
    <#
    .SYNOPSIS
        Retrieves audit events generated inside container.
    
    .DESCRIPTION
        Polls container for security events via:
        1. docker exec audit log read
        2. Docker event stream parsing
        3. Container logs (stdout/stderr)
    #>
    
    [CmdletBinding()]
    param(
        [string]$ContainerName = $Config.ContainerName,
        [switch]$Realtime,
        [int]$PollingInterval = 5
    )

    Write-AuditLog -Level INFO -Message "Retrieving container audit events" -Context @{ container = $ContainerName }

    # Method 1: Read audit log from container
    try {
        $AuditCmd = "cat $($Config.ContainerAuditPath)/events.json 2>/dev/null || echo '[]'"
        $JsonOutput = docker exec $ContainerName /bin/sh -c $AuditCmd

        if ($JsonOutput) {
            $Events = $JsonOutput | ConvertFrom-Json -AsHashtable
            Write-AuditLog -Level DEBUG -Message "Retrieved container events" -Context @{ count = $Events.Count }
            return $Events
        }
    }
    catch {
        Write-AuditLog -Level WARN -Message "Failed to read container audit log: $_"
    }

    # Method 2: Parse Docker logs
    try {
        $DockerLogs = docker logs --timestamps $ContainerName | Select-Object -Last 100
        $Events = @()

        $DockerLogs | ForEach-Object {
            if ($_ -match '\[(?<level>.*?)\](?<message>.*)') {
                $Events += @{
                    type      = 'docker.log'
                    level     = $Matches['level']
                    message   = $Matches['message']
                    timestamp = Get-Date
                }
            }
        }

        return $Events
    }
    catch {
        Write-AuditLog -Level ERROR -Message "Failed to parse Docker logs: $_"
        return @()
    }
}

function Send-ContainerAuditEvent {
    <#
    .SYNOPSIS
        Sends audit event INTO container for processing.
    #>
    
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$EventType,
        [Parameter(Mandatory)]
        [hashtable]$EventData,
        [string]$ContainerName = $Config.ContainerName
    )

    $Event = @{
        type      = $EventType
        timestamp = Get-Date -Format 'u'
        source    = 'host'
        data      = $EventData
    } | ConvertTo-Json -Compress

    Write-AuditLog -Level DEBUG -Message "Sending event to container" -Context @{ type = $EventType; container = $ContainerName }

    # Write event to container's audit FIFO/socket
    $WriteCmd = "echo '$Event' >> $($Config.ContainerAuditPath)/inbound.log"
    
    try {
        docker exec $ContainerName /bin/sh -c $WriteCmd
        Write-AuditLog -Level INFO -Message "Event delivered to container" -Context @{ type = $EventType }
    }
    catch {
        Write-AuditLog -Level ERROR -Message "Failed to deliver event to container: $_" -Context @{ type = $EventType }
    }
}

#endregion

#region TI-ULA Model Integration

function Invoke-TiUlaModel {
    <#
    .SYNOPSIS
        Executes TI-ULA threat intelligence model on audit events.
    
    .DESCRIPTION
        Processes audit events through ML models:
        1. Anomaly detection (statistical deviation)
        2. Attack pattern recognition (known CVE signatures)
        3. Behavior analysis (process chains)
        4. Privilege escalation inference
    #>
    
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [hashtable[]]$AuditEvents,
        [ValidateSet('anomaly', 'pattern_match', 'behavior', 'privilege_esc')]
        [string[]]$Models = @('anomaly', 'pattern_match'),
        [float]$AnomalyThreshold = 0.75
    )

    Write-AuditLog -Level INFO -Message "Invoking TI-ULA models" -Context @{ 
        event_count = $AuditEvents.Count
        models      = $Models -join ','
    }

    $Results = @{
        models_run    = @()
        detections    = @()
        risk_score    = 0.0
        recommendations = @()
    }

    # Model 1: Anomaly Detection
    if ('anomaly' -in $Models) {
        $AnomalyResult = Invoke-AnomalyDetectionModel -Events $AuditEvents -Threshold $AnomalyThreshold
        $Results.models_run += 'anomaly'
        $Results.detections += $AnomalyResult.detections
        $Results.risk_score = [Math]::Max($Results.risk_score, $AnomalyResult.risk_score)

        if ($AnomalyResult.detections.Count -gt 0) {
            Write-AuditLog -Level WARN -Message "Anomalies detected" -Context @{ count = $AnomalyResult.detections.Count }
        }
    }

    # Model 2: Pattern Matching
    if ('pattern_match' -in $Models) {
        $PatternResult = Invoke-PatternMatchingModel -Events $AuditEvents
        $Results.models_run += 'pattern_match'
        $Results.detections += $PatternResult.detections
        $Results.risk_score = [Math]::Max($Results.risk_score, $PatternResult.risk_score)

        if ($PatternResult.detections.Count -gt 0) {
            Write-AuditLog -Level WARN -Message "Attack patterns detected" -Context @{ patterns = $PatternResult.detections.signature }
        }
    }

    # Model 3: Behavior Analysis
    if ('behavior' -in $Models) {
        $BehaviorResult = Invoke-BehaviorAnalysisModel -Events $AuditEvents
        $Results.models_run += 'behavior'
        $Results.detections += $BehaviorResult.detections
        $Results.risk_score = [Math]::Max($Results.risk_score, $BehaviorResult.risk_score)
    }

    # Model 4: Privilege Escalation Inference
    if ('privilege_esc' -in $Models) {
        $PrivEscResult = Invoke-PrivilegeEscalationModel -Events $AuditEvents
        $Results.models_run += 'privilege_esc'
        $Results.detections += $PrivEscResult.detections
        $Results.risk_score = [Math]::Max($Results.risk_score, $PrivEscResult.risk_score)

        if ($PrivEscResult.detections.Count -gt 0) {
            Write-AuditLog -Level ERROR -Message "Privilege escalation attempt detected" -Context @{ count = $PrivEscResult.detections.Count }
        }
    }

    $Results.timestamp = Get-Date -Format 'u'
    return $Results
}

function Invoke-AnomalyDetectionModel {
    <#
    .SYNOPSIS
        Statistical anomaly detection on audit event stream.
    
    .NOTES
        Baseline: Normal event frequency per minute
        Anomaly: Events > 3σ (99.7% confidence)
    #>
    
    param(
        [hashtable[]]$Events,
        [float]$Threshold = 0.75
    )

    $EventCounts = @{}
    $Events | Group-Object -Property type | ForEach-Object {
        $EventCounts[$_.Name] = $_.Count
    }

    $Mean = ($EventCounts.Values | Measure-Object -Average).Average
    $StdDev = [Math]::Sqrt(($EventCounts.Values | ForEach-Object { [Math]::Pow($_ - $Mean, 2) } | Measure-Object -Average).Average)
    $Threshold3Sigma = $Mean + (3 * $StdDev)

    $Detections = @()
    $RiskScore = 0.0

    $EventCounts.GetEnumerator() | ForEach-Object {
        if ($_.Value -gt $Threshold3Sigma) {
            $ZScore = ($_.Value - $Mean) / [Math]::Max($StdDev, 0.001)
            $Risk = [Math]::Min(1.0, $ZScore / 3)

            $Detections += @{
                type        = 'anomalous_event_frequency'
                event_type  = $_.Key
                count       = $_.Value
                z_score     = [Math]::Round($ZScore, 2)
                severity    = if ($Risk -gt 0.8) { 'HIGH' } elseif ($Risk -gt 0.5) { 'MEDIUM' } else { 'LOW' }
            }

            $RiskScore = [Math]::Max($RiskScore, $Risk)
        }
    }

    return @{
        detections = $Detections
        risk_score = $RiskScore
    }
}

function Invoke-PatternMatchingModel {
    <#
    .SYNOPSIS
        Matches audit events against known attack signatures.
    #>
    
    param([hashtable[]]$Events)

    $AttackSignatures = @(
        @{
            name    = 'Directory Traversal'
            pattern = '\.\.[\\/]'
            severity = 'HIGH'
        },
        @{
            name    = 'Command Injection'
            pattern = '[;&|`$(){}]'
            severity = 'HIGH'
        },
        @{
            name    = 'Privilege Escalation Attempt'
            pattern = 'sudo|SeTcbPrivilege|CAP_SYS_ADMIN'
            severity = 'CRITICAL'
        },
        @{
            name    = 'Credential Access'
            pattern = 'password|token|key|secret|credential'
            severity = 'HIGH'
        }
    )

    $Detections = @()
    $MaxRisk = 0.0

    $Events | ForEach-Object {
        $EventStr = $_ | ConvertTo-Json
        
        $AttackSignatures | ForEach-Object {
            if ($EventStr -match $_.pattern) {
                $SeverityScore = @{ CRITICAL = 1.0; HIGH = 0.8; MEDIUM = 0.5; LOW = 0.2 }[$_.severity]
                $MaxRisk = [Math]::Max($MaxRisk, $SeverityScore)

                $Detections += @{
                    type      = 'attack_pattern_match'
                    signature = $_.name
                    severity  = $_.severity
                    event     = $_
                }
            }
        }
    }

    return @{
        detections = $Detections
        risk_score = $MaxRisk
    }
}

function Invoke-BehaviorAnalysisModel {
    param([hashtable[]]$Events)
    
    # Placeholder: Real implementation would use ML model
    return @{
        detections = @()
        risk_score = 0.0
    }
}

function Invoke-PrivilegeEscalationModel {
    param([hashtable[]]$Events)

    $PrivEscIndicators = @(
        'sudo',
        'SeTcbPrivilege',
        'CAP_SYS_ADMIN',
        'setuid',
        'setcap',
        'LD_PRELOAD',
        'selinux disabled'
    )

    $Detections = @()
    $MaxRisk = 0.0

    $Events | ForEach-Object {
        $EventStr = $_ | ConvertTo-Json

        $PrivEscIndicators | ForEach-Object {
            if ($EventStr -match $_) {
                $MaxRisk = 1.0
                $Detections += @{
                    type      = 'privilege_escalation_indicator'
                    indicator = $_
                    severity  = 'CRITICAL'
                    event     = $_
                }
            }
        }
    }

    return @{
        detections = $Detections
        risk_score = $MaxRisk
    }
}

#endregion

#region Reporting & Response

function New-AuditReport {
    <#
    .SYNOPSIS
        Generates comprehensive audit report with TI-ULA insights.
    #>
    
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [hashtable]$TiUlaResults,
        [string]$ContainerName = $Config.ContainerName,
        [string]$OutputPath = $Config.HostAuditPath
    )

    $Report = @{
        report_id        = [guid]::NewGuid().ToString()
        timestamp        = Get-Date -Format 'u'
        container        = $ContainerName
        ti_ula_results   = $TiUlaResults
        risk_level       = if ($TiUlaResults.risk_score -ge 0.8) { 'CRITICAL' } 
                          elseif ($TiUlaResults.risk_score -ge 0.5) { 'HIGH' }
                          elseif ($TiUlaResults.risk_score -ge 0.25) { 'MEDIUM' }
                          else { 'LOW' }
        actions_recommended = Get-RecommendedActions -Results $TiUlaResults
    }

    $ReportPath = Join-Path -Path $OutputPath -ChildPath "audit_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
    
    if ($Config.EnableCrypto) {
        $JsonReport = $Report | ConvertTo-Json -Depth 10
        $Encrypted = Protect-AuditData -Data $JsonReport
        Set-Content -Path $ReportPath -Value $Encrypted -Encoding UTF8
        Write-AuditLog -Level INFO -Message "Encrypted audit report saved" -Context @{ path = $ReportPath }
    }
    else {
        $Report | ConvertTo-Json -Depth 10 | Set-Content -Path $ReportPath
        Write-AuditLog -Level INFO -Message "Audit report saved" -Context @{ path = $ReportPath }
    }

    return $Report
}

function Get-RecommendedActions {
    param([hashtable]$Results)

    $Actions = @()

    if ($Results.risk_score -ge 0.8) {
        $Actions += "ISOLATE: Container shows signs of compromise. Recommend immediate isolation."
        $Actions += "INVESTIGATE: Review all network connections and file modifications."
        $Actions += "BLOCK: Consider blocking container from external network."
    }
    elseif ($Results.risk_score -ge 0.5) {
        $Actions += "MONITOR: Increase monitoring frequency to 1x per minute."
        $Actions += "REVIEW: Audit recent container execution logs."
        $Actions += "RESTRICT: Tighten resource limits if not already done."
    }
    elseif ($Results.detections.Count -gt 0) {
        $Actions += "DOCUMENT: Log detection for compliance audit trail."
        $Actions += "ALERT: Send alert to security team for review."
    }

    return $Actions
}

function Protect-AuditData {
    param([Parameter(Mandatory)][string]$Data)

    # Encrypt using Windows DPAPI (user-level encryption)
    $Bytes = [Text.Encoding]::UTF8.GetBytes($Data)
    $EncryptedBytes = [Security.Cryptography.ProtectedData]::Protect($Bytes, $null, [Security.Cryptography.DataProtectionScope]::CurrentUser)
    return [Convert]::ToBase64String($EncryptedBytes)
}

#endregion

#region Main Orchestration

function Start-TiUlaBridge {
    <#
    .SYNOPSIS
        Starts the TI-ULA audit bridge service.
    
    .DESCRIPTION
        Continuously monitors container and sends audit events through TI-ULA models.
    #>
    
    [CmdletBinding()]
    param(
        [int]$PollingIntervalSeconds = 10,
        [switch]$Continuous
    )

    Write-AuditLog -Level INFO -Message "Starting TI-ULA audit bridge" -Context @{ 
        container = $Config.ContainerName
        polling_interval = $PollingIntervalSeconds
    }

    # Ensure directories exist
    @($Config.HostAuditPath, $Config.TiUlaModelPath) | ForEach-Object {
        if (-not (Test-Path -Path $_)) {
            New-Item -ItemType Directory -Path $_ -Force | Out-Null
        }
    }

    $IterationCount = 0
    
    do {
        $IterationCount++
        
        try {
            # 1. Retrieve container audit events
            $ContainerEvents = Get-ContainerAuditEvents -ContainerName $Config.ContainerName
            
            if ($ContainerEvents.Count -eq 0) {
                Write-AuditLog -Level DEBUG -Message "No container events retrieved" -Context @{ iteration = $IterationCount }
            }
            else {
                Write-AuditLog -Level DEBUG -Message "Retrieved container events" -Context @{ count = $ContainerEvents.Count }

                # 2. Invoke TI-ULA models
                $TiUlaResults = Invoke-TiUlaModel -AuditEvents $ContainerEvents

                # 3. Generate report
                $Report = New-AuditReport -TiUlaResults $TiUlaResults

                # 4. Send recommendations back to container (if risky)
                if ($Report.risk_level -in @('HIGH', 'CRITICAL')) {
                    Send-ContainerAuditEvent -EventType $AuditEventTypes.ANOMALY_DETECTED -EventData @{
                        risk_level = $Report.risk_level
                        risk_score = $TiUlaResults.risk_score
                        actions    = $Report.actions_recommended
                    }

                    Write-AuditLog -Level WARN -Message "High-risk detection sent to container" -Context @{ risk_level = $Report.risk_level }
                }
            }

            # 5. Sleep before next iteration
            Start-Sleep -Seconds $PollingIntervalSeconds
        }
        catch {
            Write-AuditLog -Level ERROR -Message "Error in bridge iteration: $_" -Context @{ iteration = $IterationCount }
        }

    } while ($Continuous)

    Write-AuditLog -Level INFO -Message "TI-ULA audit bridge stopped" -Context @{ iterations = $IterationCount }
}

#endregion

Export-ModuleMember -Function @(
    'Start-TiUlaBridge',
    'Get-ContainerAuditEvents',
    'Send-ContainerAuditEvent',
    'Invoke-TiUlaModel',
    'New-AuditReport',
    'Write-AuditLog'
)
