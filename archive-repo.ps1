<#
archive-repo.ps1
Utility to create a reliable archive of a git repository for forensic backup.
Usage example:
  .\archive-repo.ps1 -RepoPath 'C:\path\to\repo' -BackupDir 'H:\ACTOR_DEV_ENV\Backups' -ExcludeDirs '.venv','node_modules'

Behavior:
- Copies repository to a temporary location using robocopy while excluding common large dirs
- Compresses the copy with 7z if available, otherwise Compress-Archive
- Computes SHA256 and makes the archive read-only
- Optionally appends an entry to git_archive_manifest.json in the repo root
#>
param(
    [Parameter(Mandatory=$true)][string]$RepoPath,
    [Parameter(Mandatory=$true)][string]$BackupDir,
    [string[]]$ExcludeDirs = @('.venv','venv','node_modules','.cache'),
    [string]$SevenZipPath = 'C:\Program Files\7-Zip\7z.exe',
    [switch]$KeepTemp
)

function Write-Log { param($m) Write-Host "[archive-repo] $m" }

if (-not (Test-Path $RepoPath)) { Write-Error "Repo path not found: $RepoPath"; exit 2 }
if (-not (Test-Path $BackupDir)) { New-Item -Path $BackupDir -ItemType Directory -Force | Out-Null }

$repoName = (Split-Path $RepoPath -Leaf) -replace '[^A-Za-z0-9_.-]','_'
$time = Get-Date -Format 'yyyyMMdd_HHmmss'
$temp = Join-Path $env:TEMP "$repoName-temp-$time"
$copyDest = $temp

# Build robocopy exclude args
$xdArgs = @()
foreach ($d in $ExcludeDirs) { $xdArgs += '/XD'; $xdArgs += (Join-Path $RepoPath $d) }

Write-Log "Copying repository (robocopy) to temporary folder: $copyDest"
# Robocopy /MIR mirrors, /R:1 /W:1 minimal retries
$rcArgs = @($RepoPath, $copyDest, '/MIR', '/R:1', '/W:1', '/NFL','/NDL') + $xdArgs
$rc = Start-Process -FilePath robocopy -ArgumentList $rcArgs -NoNewWindow -Wait -PassThru
if ($rc.ExitCode -ge 8) {
    Write-Warning "Robocopy reported a failure code: $($rc.ExitCode)" # non-fatal but warn
}

# Ensure target archive filename
$zipName = "$repoName`_$time.zip"
$zipPath = Join-Path $BackupDir $zipName

if (Test-Path $SevenZipPath) {
    Write-Log "7-Zip found at $SevenZipPath — using it to create archive"
    $sevenArgs = @('a','-tzip',"$zipPath","$copyDest\*")
    $p = Start-Process -FilePath $SevenZipPath -ArgumentList $sevenArgs -NoNewWindow -Wait -PassThru
    if ($p.ExitCode -ne 0) { Write-Warning "7-Zip exited with code $($p.ExitCode). Falling back to Compress-Archive."; Remove-Item -Recurse -Force $zipPath -ErrorAction SilentlyContinue; goto CompressFallback }
} else {
    :CompressFallback
    Write-Log "7-Zip not found — using Compress-Archive (may require sufficient memory)"
    try {
        Compress-Archive -Path (Join-Path $copyDest '*') -DestinationPath $zipPath -Force -ErrorAction Stop
    } catch {
        Write-Error "Compress-Archive failed: $($_.Exception.Message)"
        Remove-Item -Recurse -Force $copyDest -ErrorAction SilentlyContinue
        exit 3
    }
}

# Compute SHA256
try {
    $hash = (Get-FileHash -Path $zipPath -Algorithm SHA256).Hash
    Write-Log "Archive created: $zipPath (SHA256: $hash)"
    # make read-only
    $f = Get-Item $zipPath
    $f.Attributes = $f.Attributes -bor [System.IO.FileAttributes]::ReadOnly
} catch {
    Write-Warning "Failed to compute hash or set readonly: $($_.Exception.Message)"
}

# Append to manifest if present in repo root
$manifestPath = Join-Path (Get-Location) 'git_archive_manifest.json'
if (Test-Path $manifestPath) {
    try {
        $existing = Get-Content $manifestPath -Raw | ConvertFrom-Json -ErrorAction Stop
    } catch { $existing = $null }
    $entry = [PSCustomObject]@{
        Repo = $RepoPath
        ArchivePath = $zipPath
        SHA256 = $hash
        CreatedAt = (Get-Date).ToString('o')
        Status = 'archived'
    }
    if ($existing -is [Array]) { $new = $existing + $entry } elseif ($existing -ne $null) { $new = @($existing,$entry) } else { $new = @($entry) }
    $new | ConvertTo-Json -Depth 5 | Set-Content -Path $manifestPath -Encoding UTF8
    Write-Log "Appended manifest entry to $manifestPath"
} else {
    Write-Log "Manifest not found at repo root ($manifestPath). Skipping auto-append."
}

if (-not $KeepTemp) { Remove-Item -Recurse -Force $copyDest -ErrorAction SilentlyContinue }

Write-Log "Done."

# Exit codes: 0=ok, 2=repo not found, 3=compress failed
