
$manifestPath = "apostille-mirror\mcp_forensic_manifest.json"
$reportPath = "apostille-mirror\forensic_reports\INTEGRITY_CHECK_20260615.json"
$baseDir = "H:\ACTOR_DEV_ENV\apostille-mirror"

if (-Not (Test-Path $manifestPath)) {
    Write-Error "Manifest not found: $manifestPath"
    exit 1
}

$manifestJson = Get-Content $manifestPath -Raw | ConvertFrom-Json
$results = New-Object System.Collections.Generic.List[PSObject]

foreach ($node in $manifestJson.nodes) {
    $fullPath = Join-Path $baseDir $node.rel_path
    $status = "UNKNOWN"
    $actualHash = "N/A"

    if (Test-Path $fullPath -PathType Leaf) {
        $actualHash = (Get-FileHash -Path $fullPath -Algorithm SHA256).Hash
        if ($actualHash -eq $node.sha256) {
            $status = "MATCH"
        } else {
            $status = "MISMATCH"
        }
    } else {
        $status = "MISSING"
    }

    $results.Add([PSCustomObject]@{
        File = $node.rel_path
        Expected = $node.sha256
        Actual = $actualHash
        Status = $status
    })
}

$results | ConvertTo-Json -Depth 5 | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Integrity report saved to $reportPath"
$results | Where-Object { $_.Status -ne "MATCH" } | Format-Table -AutoSize
