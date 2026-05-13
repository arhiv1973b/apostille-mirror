# A©tor Seamless Reconnection Protocol
# Автоматическая проверка и восстановление инфраструктуры

Write-Host "[*] Инициация протокола бесшовного переподключения..." -ForegroundColor Cyan

# 1. Проверка Ollama и моделей
$Model = "qwen2.5:3b"
Write-Host "[*] Проверка модели $Model..."
$OllamaCheck = ollama list | Select-String -Pattern $Model
if (-not $OllamaCheck) {
    Write-Host "[!] Модель не найдена. Скачивание..." -ForegroundColor Yellow
    ollama pull $Model
} else {
    Write-Host "[OK] Модель активна." -ForegroundColor Green
}

# 2. Проверка и пересборка Docker шлюза
Write-Host "[*] Валидация контейнера gateway-agent..."
$DockerStatus = docker ps -a --filter "name=gateway-agent" -q
if ($DockerStatus) {
    docker rm -f gateway-agent | Out-Null
}
docker build -t gateway-agent gateway_agent/ | Out-Null
Write-Host "[OK] Шлюз пересобран и готов." -ForegroundColor Green

# 3. Обновление команд и алиасов
# Убеждаемся, что функция gemini доступна
function gemini {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Query)
    $QueryString = $Query -join " "
    docker run --rm gateway-agent python proxy_logic.py $QueryString
}

Write-Host "[!] Протокол переподключения завершен. Система A©tor синхронизирована." -ForegroundColor Green
