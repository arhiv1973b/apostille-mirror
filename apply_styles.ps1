# 1. Задаем пути (Используем ваш путь из слепка)
$repoPath = "H:\ACTOR_DEV_ENV\copilot-worktrees\apostille-mirror\arhiv1973b-automatic-invention"
$cssLink = '<link rel="stylesheet" href="unified-theme.css">'

# 2. Ищем все HTML файлы
$htmlFiles = Get-ChildItem -Path $repoPath -Filter "*.html" -Recurse

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    
    # Если файл содержит блок <style> и не содержит линк на наш CSS
    if ($content -match '(?s)<style>.*?</style>' -and $content -notmatch 'unified-theme\.css') {
        Write-Host "Обновление стилей в: $($file.Name)" -ForegroundColor Cyan
        
        # Заменяем весь блок <style> на ссылку на внешний файл
        $newContent = $content -replace '(?s)<style>.*?</style>', $cssLink
        
        # Сохраняем файл обратно (важно сохранять в UTF8 без BOM для Git)
        $Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding $False
        [System.IO.File]::WriteAllText($file.FullName, $newContent, $Utf8NoBomEncoding)
    }
}

# 3. Легковесная оптимизация Git (без триггера полной перепаковки для облака)
Write-Host "Запуск очистки мусора Git..." -ForegroundColor Yellow
Set-Location -Path $repoPath
git gc --auto
git prune

Write-Host "Готово! Проверьте `git status` и `git diff`." -ForegroundColor Green
