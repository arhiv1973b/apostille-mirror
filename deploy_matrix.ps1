Set-Location "H:\Загрузки\MACHERET_SITE_DEPLOY"
Write-Host "[1/3] Запуск IMAP Monitor..." -ForegroundColor Cyan
python matrix_monitor.py
Write-Host "[2/3] GPG-подпись и фиксация ВСЕХ файлов..." -ForegroundColor Cyan
$env:GPG_TTY = "tty"
# Добавляем скрипты и документы в индекс
git add response_matrix.json matrix_monitor.py deploy_matrix.ps1 liability_notice_final_0205.*
git commit -S -m "A©TOR · TOTAL INTEGRITY · Recovery BOM Fix · All docs synced · IDNP 655"
Write-Host "[3/3] Синхронизация с Forensic Evidence Vault..." -ForegroundColor Cyan
git pull --rebase origin main
git push origin main
Write-Host "✅ Система полностью синхронизирована и запечатана." -ForegroundColor Green