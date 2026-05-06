Write-Host "--- A©t0r GPG REPAIR PROTOCOL ---" -ForegroundColor Cyan
Write-Host "1. Killing existing gpg-agents..." -ForegroundColor Yellow
taskkill /IM gpg-agent.exe /F 2>$null

Write-Host "2. Clearing git index locks..." -ForegroundColor Yellow
if (Test-Path ".git/index.lock") { Remove-Item ".git/index.lock" -Force }

Write-Host "3. Restarting gpg-connect-agent..." -ForegroundColor Yellow
gpg-connect-agent reloadagent /bye

Write-Host "4. Testing signing for A©tor key..." -ForegroundColor Yellow
echo "test" | gpg --clearsign --local-user 87B7956E898ED56D74EDD1D05B1948C896CCCECE
