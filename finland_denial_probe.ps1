$targets = @('https://justice.gov.md', 'https://cnas.md', 'https://micb.md')
$logPath = "$env:USERPROFILE\Finland_Denial_Audit.log"

Write-Host "--- МОНИТОРИНГ 'ФИНЛЯНДИЯ' (GROUP I VULNERABILITY) ЗАПУЩЕН ---" -ForegroundColor Cyan
Write-Host "Лог: $logPath" -ForegroundColor Gray

while($true) {
    foreach ($url in $targets) {
        try {
            $response = Invoke-WebRequest -Uri $url -Method Head -TimeoutSec 10 -ErrorAction Stop -UseBasicParsing
            $status = "OK: $($response.StatusCode)"
            $color = "Green"
        } catch {
            $status = "DENIAL: $($_.Exception.Message)"
            $color = "Red"
        }
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $entry = "[$timestamp] Target: $url | Status: $status | Priority: Critical (Group I)"
        
        Add-Content -Path $logPath -Value $entry
        Write-Host $entry -ForegroundColor $color
    }
    Write-Host "Ожидание 5 минут..." -ForegroundColor DarkGray
    Start-Sleep -Seconds 300
}
