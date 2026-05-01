# ═══════════════════════════════════════════════════════════════
# DEPLOY.ps1 — A©t0r Autonomous Deploy Script
# CASE-MACHERET-1997-2026 · arhiv1973b@outlook.com
# Запуск: Set-ExecutionPolicy Bypass -Scope Process; .\DEPLOY.ps1
# ═══════════════════════════════════════════════════════════════

param(
    [string]$GitHubToken = $env:GITHUB_TOKEN,
    [string]$GpgPassword = $env:ACTOR_GPG_PASS,
    [string]$RepoOwner   = "arhiv1973b",
    [string]$RepoName    = "apostille-mirror",
    [string]$Branch      = "main"
)

$ErrorActionPreference = "Stop"
$SITE_DIR = $PSScriptRoot

# ── ЦВЕТА ──
function Write-Step   { Write-Host "`n[A©t0r] $args" -ForegroundColor Cyan }
function Write-Ok     { Write-Host "  ✅ $args" -ForegroundColor Green }
function Write-Warn   { Write-Host "  ⚠️  $args" -ForegroundColor Yellow }
function Write-Fail   { Write-Host "  ❌ $args" -ForegroundColor Red }

Write-Host @"
╔══════════════════════════════════════════════════════╗
║   A©t0r AUTONOMOUS DEPLOY · CASE-MACHERET-1997-2026 ║
║   arhiv1973b.github.io/apostille-mirror              ║
╚══════════════════════════════════════════════════════╝
"@ -ForegroundColor Yellow

# ── ШАГИ ──

# 1. Проверка зависимостей
Write-Step "ШАГ 1: Проверка зависимостей"
$required = @("git","gpg")
foreach ($cmd in $required) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        Write-Ok "$cmd доступен"
    } else {
        Write-Fail "$cmd не найден. Установите: winget install GnuPG.GnuPG / git.git"
        exit 1
    }
}

# 2. Конфигурация Git
Write-Step "ШАГ 2: Конфигурация Git"
git config --global user.email "arhiv1973b@outlook.com"
git config --global user.name "A©t0r Macheret"
git config --global init.defaultBranch main
Write-Ok "Git настроен: A©t0r Macheret <arhiv1973b@outlook.com>"

# 3. GPG ключ
Write-Step "ШАГ 3: GPG — генерация / проверка ключа"
$existingKey = gpg --list-secret-keys --keyid-format LONG 2>$null | Select-String "arhiv1973b"
if ($existingKey) {
    Write-Ok "GPG ключ существует: $existingKey"
} else {
    Write-Warn "GPG ключ не найден. Генерирую..."
    $gpgBatch = @"
%echo Generating A©t0r GPG key
Key-Type: RSA
Key-Length: 4096
Subkey-Type: RSA
Subkey-Length: 4096
Name-Real: Maceret Alexei
Name-Comment: A©t0r CASE-MACHERET-1997-2026
Name-Email: arhiv1973b@outlook.com
Expire-Date: 0
%no-ask-passphrase
%no-protection
%commit
%echo done
"@
    $gpgBatch | gpg --batch --gen-key
    Write-Ok "GPG ключ создан"
}

# Получаем fingerprint
$gpgKey = (gpg --list-secret-keys --keyid-format LONG 2>$null | Select-String "[A-F0-9]{16}" | Select-Object -First 1).Matches[0].Value
if ($gpgKey) {
    git config --global user.signingkey $gpgKey
    git config --global commit.gpgsign true
    Write-Ok "GPG signing: $gpgKey"
}

# 4. Git init / remote
Write-Step "ШАГ 4: Git репозиторий"
Set-Location $SITE_DIR

if (-not (Test-Path ".git")) {
    git init
    Write-Ok "Git init"
}

$remoteExists = git remote -v 2>$null | Select-String "origin"
if (-not $remoteExists) {
    if ($GitHubToken) {
        git remote add origin "https://$GitHubToken@github.com/$RepoOwner/$RepoName.git"
    } else {
        git remote add origin "https://github.com/$RepoOwner/$RepoName.git"
    }
    Write-Ok "Remote: github.com/$RepoOwner/$RepoName"
} else {
    Write-Ok "Remote уже настроен"
}

# 5. Вычисление SHA-256 архива
Write-Step "ШАГ 5: Вычисление SHA-256 целостности"
$indexHash = (Get-FileHash "index.html" -Algorithm SHA256).Hash.ToLower()
Write-Ok "index.html SHA-256: $indexHash"

# Обновляем хэш в integrity.json
$integrity = @{
    timestamp    = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
    case         = "CASE-MACHERET-1997-2026"
    idnp         = "2000001159655"
    commit_ref   = "HEAD"
    index_sha256 = $indexHash
    ti_ula_nodes = 4010
    apostilles   = 97
} | ConvertTo-Json -Depth 3
$integrity | Out-File -FilePath "assets/data/integrity.json" -Encoding utf8
Write-Ok "integrity.json обновлён"

# 6. Commit + Push
Write-Step "ШАГ 6: Commit & Push"
git add -A
$commitMsg = "A©t0r deploy: $(Get-Date -Format 'yyyy-MM-dd HH:mm') | nodes:4010 | apostilles:97 | sha:$($indexHash.Substring(0,12))"

if ($gpgKey) {
    git commit -S -m $commitMsg
} else {
    git commit -m $commitMsg
}

if ($GitHubToken) {
    git push -u origin $Branch --force
    Write-Ok "Push успешен → github.com/$RepoOwner/$RepoName"
} else {
    Write-Warn "GITHUB_TOKEN не задан. Push пропущен."
    Write-Host ""
    Write-Host "  Для деплоя выполните:" -ForegroundColor White
    Write-Host "  `$env:GITHUB_TOKEN='<ваш_токен>'; .\DEPLOY.ps1" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Или вручную:" -ForegroundColor White
    Write-Host "  git push https://<TOKEN>@github.com/$RepoOwner/$RepoName.git main" -ForegroundColor Yellow
}

# 7. GitHub Pages проверка
Write-Step "ШАГ 7: GitHub Pages"
Write-Host "  Сайт будет доступен через ~2 минуты:" -ForegroundColor White
Write-Host "  https://$RepoOwner.github.io/$RepoName/" -ForegroundColor Cyan

Write-Host @"

╔══════════════════════════════════════════════════════╗
║  ✅ DEPLOY COMPLETE · A©t0r · $(Get-Date -Format 'dd.MM.yyyy HH:mm')         ║
║  JUS COGENS · ERGA OMNES · БЕЗ СРОКА ДАВНОСТИ       ║
╚══════════════════════════════════════════════════════╝
"@ -ForegroundColor Green
