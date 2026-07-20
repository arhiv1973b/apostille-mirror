@echo off
chcp 65001 >nul
title ⚖️ DEPLOY — apostille-legal-case → GitHub Pages

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║  A©TOR DEPLOY AGENT — CASE-MACHERET-1997-2026       ║
echo ║  GitHub Pages Auto-Deploy                            ║
echo ╚══════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM ── Проверка git ──
where git >nul 2>&1
if errorlevel 1 (
  echo [ERROR] git не найден. Установите Git for Windows.
  pause & exit /b 1
)

echo [1/6] Статус репозитория...
git status --short
echo.

echo [2/6] Добавляем новые HTML файлы агента...
git add docs-agent-navigator.html
git add 404.html
git add sitemap.xml
git add _config.yml
git add _headers

REM Добавляем все изменённые .html .md .json файлы
git add -u
git add *.html
git add *.md
git add *.json
git add docs/

echo [3/6] Проверяем что добавлено...
git diff --cached --name-only
echo.

echo [4/6] Коммит...
git commit -m "deploy: add tunnel navigator agent + fix DULCHA name + update 404 + sitemap [2026-03-30]"

if errorlevel 1 (
  echo [INFO] Нечего коммитить или уже актуально.
)

echo [5/6] Push в master...
git push origin master

if errorlevel 1 (
  echo.
  echo [WARN] Push в master не удался. Пробуем main...
  git push origin main
)

echo.
echo [6/6] Merge / Deploy проверка...
echo GitHub Pages задеплоит автоматически через ~60 секунд после push.
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║  LIVE URL:                                           ║
echo ║  https://arhiv1973b.github.io/apostille-legal-case/ ║
echo ║  docs-agent-navigator.html                           ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo Нажмите любую клавишу для проверки статуса деплоя...
pause >nul

REM Открываем браузер на странице навигатора
start "" "https://arhiv1973b.github.io/apostille-legal-case/docs-agent-navigator.html"

echo.
echo [DONE] Деплой завершён!
echo ДУЛЧА В.Г. — имя исправлено в навигаторе.
echo 404 → туннельный редирект на RAW GitHub.
echo.
pause
