$repositories = @(
    "F:\Projects\apostille-archive-english",
    "H:\ACTOR_DEV_ENV\copilot-worktrees\apostille-mirror"
)

$outputFile = "repo_audit_manifest.json"
$results = @()

foreach ($repo in $repositories) {
    if (Test-Path $repo) {
        $files = Get-ChildItem -Path $repo -Recurse -File | Where-Object { $_.Extension -match '\.(html|css|js|md)' }
        foreach ($file in $files) {
            $content = ""
            if ($file.Length -lt 10240) {
                $content = Get-Content -Path $file.FullName -Raw
            }
            $results += [PSCustomObject]@{
                Path    = $file.FullName
                Repo    = (Split-Path $repo -Leaf)
                Size    = $file.Length
                Content = $content
            }
        }
    }
}

$results | ConvertTo-Json -Depth 3 | Out-File -FilePath $outputFile -Encoding utf8
Write-Host "Аудит завершен. Данные сохранены в $outputFile" -ForegroundColor Cyan
