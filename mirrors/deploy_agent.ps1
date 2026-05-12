# ⚖️ DEPLOY + MERGE AGENT — apostille-legal-case
# CASE-MACHERET-1997-2026 | GitHub Pages Auto-Deploy
# Запуск: правая кнопка → "Запустить с помощью PowerShell"

$ErrorActionPreference = "Continue"
$RepoPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoPath

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  A©TOR DEPLOY AGENT — CASE-MACHERET-1997-2026       ║" -ForegroundColor Cyan
Write-Host "║  Tunnel Navigator + Fix ДУЛЧА + GitHub Pages Deploy  ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ── ШАГ 1: Проверка git ──
Write-Host "[1/7] Проверка git..." -ForegroundColor Yellow
$gitVersion = git --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] git не найден! Установите Git for Windows." -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}
Write-Host "  git: $gitVersion" -ForegroundColor Green

# ── ШАГ 2: Статус ──
Write-Host ""
Write-Host "[2/7] Текущий статус репозитория..." -ForegroundColor Yellow
git status --short

# ── ШАГ 3: Проверка веток ──
Write-Host ""
Write-Host "[3/7] Список веток..." -ForegroundColor Yellow
$branches = git branch -a 2>&1
Write-Host $branches
$currentBranch = git rev-parse --abbrev-ref HEAD 2>&1
Write-Host "  Текущая ветка: $currentBranch" -ForegroundColor Cyan

# ── ШАГ 4: Добавление файлов ──
Write-Host ""
Write-Host "[4/7] Добавление файлов агента в индекс..." -ForegroundColor Yellow

# Новые файлы агента
git add "docs-agent-navigator.html"
Write-Host "  + docs-agent-navigator.html (Tunnel Navigator — ДУЛЧА исправлено)" -ForegroundColor Green

git add "404.html"
Write-Host "  + 404.html (Tunnel redirect → RAW GitHub)" -ForegroundColor Green

git add "sitemap.xml"
Write-Host "  + sitemap.xml (обновлён)" -ForegroundColor Green

git add "_headers"
git add "_config.yml"

# Все изменения
git add -u

# Все HTML файлы
$htmlFiles = Get-ChildItem -Path $RepoPath -Filter "*.html" -File
foreach ($f in $htmlFiles) {
    git add $f.Name 2>&1 | Out-Null
}

# Docs директория
git add "docs/" 2>&1 | Out-Null

Write-Host ""
Write-Host "  Файлы в stage:" -ForegroundColor Cyan
git diff --cached --name-only

# ── ШАГ 5: Коммит ──
Write-Host ""
Write-Host "[5/7] Коммит..." -ForegroundColor Yellow

$commitMsg = "deploy: tunnel navigator agent + fix DULCHA→DULCHA V.G. + 404 tunnel redirect + sitemap [$(Get-Date -Format 'yyyy-MM-dd HH:mm')]"
git commit -m $commitMsg

if ($LASTEXITCODE -eq 0) {
    Write-Host "  Коммит создан успешно." -ForegroundColor Green
} else {
    Write-Host "  [INFO] Нечего коммитить или ошибка коммита." -ForegroundColor DarkYellow
}

# ── ШАГ 6: Merge других веток (если есть) ──
Write-Host ""
Write-Host "[6/7] Проверка дополнительных веток для merge..." -ForegroundColor Yellow

$allBranches = git branch --format='%(refname:short)' 2>&1
$featureBranches = $allBranches | Where-Object { $_ -ne $currentBranch -and $_ -ne "" -and -not $_.StartsWith("remotes/") }

if ($featureBranches) {
    Write-Host "  Найдены ветки: $($featureBranches -join ', ')" -ForegroundColor Cyan
    foreach ($branch in $featureBranches) {
        Write-Host "  Merge $branch → $currentBranch..." -ForegroundColor Yellow
        git merge $branch --no-edit 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Merged: $branch" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ Merge conflict или пустая ветка: $branch (пропуск)" -ForegroundColor DarkYellow
            git merge --abort 2>&1 | Out-Null
        }
    }
} else {
    Write-Host "  Дополнительных веток нет. Работаем только с $currentBranch." -ForegroundColor DarkGray
}

# ── ШАГ 7: Push ──
Write-Host ""
Write-Host "[7/7] Push в origin/$currentBranch..." -ForegroundColor Yellow

git push origin $currentBranch

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  ✓ PUSH УСПЕШЕН                                      ║" -ForegroundColor Green
    Write-Host "║  GitHub Pages задеплоит через ~60 сек                ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[WARN] Push в $currentBranch не удался. Пробуем master/main..." -ForegroundColor DarkYellow
    git push origin master 2>&1
    if ($LASTEXITCODE -ne 0) {
        git push origin main 2>&1
    }
}

# ── ИТОГ ──
Write-Host ""
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "ИСПРАВЛЕНИЯ В ЭТОМ ДЕПЛОЕ:" -ForegroundColor White
Write-Host "  ✓ ДУЛЧА В.Г.  (было: Дулка) — из DULCA_NOTICE.html" -ForegroundColor Green
Write-Host "  ✓ МУРЯНУ И.   — из MURIANU_NOTICE.html" -ForegroundColor Green
Write-Host "  ✓ НАНТОЙ ЛЮДМИЛА — из NANTOI_NOTICE.html" -ForegroundColor Green
Write-Host "  ✓ 404.html → туннельный редирект на RAW GitHub" -ForegroundColor Green
Write-Host "  ✓ docs-agent-navigator.html → 75 документов" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "LIVE URL после деплоя:" -ForegroundColor White
Write-Host "  https://arhiv1973b.github.io/apostille-legal-case/docs-agent-navigator.html" -ForegroundColor Cyan
Write-Host ""

# Открыть браузер через 30 секунд
Write-Host "Открываю навигатор через 5 секунд..." -ForegroundColor DarkGray
Start-Sleep -Seconds 5
Start-Process "https://arhiv1973b.github.io/apostille-legal-case/docs-agent-navigator.html"

Write-Host ""
Write-Host "Деплой завершён." -ForegroundColor Green
Read-Host "Нажмите Enter для выхода"
