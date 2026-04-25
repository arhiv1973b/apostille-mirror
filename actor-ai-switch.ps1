param(
    [switch]$List,
    [switch]$Install,
    [string]$Model = "gemini-2.5-flash",
    [string]$Query = ""
)

$MODELS = @{
    "gemini"   = "models/gemini-2.5-flash"
    "gemini3"  = "models/gemini-3-flash-preview"
    "claude"   = "claude-sonnet-4-6"
    "grok"     = "grok-2-latest"
    "openai"   = "gpt-4o"
}

if ($List) {
    Write-Host "`n📋 Доступные модели A©t0r Engine:" -ForegroundColor Cyan
    $MODELS.GetEnumerator() | ForEach-Object {
        Write-Host "  $($_.Key) → $($_.Value)" -ForegroundColor Green
    }
    Write-Host ""
    return
}

if ($Install) {
    Write-Host "📦 Установка зависимостей A©t0r..." -ForegroundColor Cyan
    pip install google-generativeai openai anthropic --quiet
    Write-Host "✅ Зависимости установлены." -ForegroundColor Green
    return
}

if ($Query) {
    Write-Host "🤖 Запрос к модели: $Model" -ForegroundColor Yellow
    $apiKey = $env:GOOGLE_GENERATIVE_AI_API_KEY

    $body = @{
        contents = @(@{ parts = @(@{ text = $Query }) })
    } | ConvertTo-Json -Depth 5

    $url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$apiKey"

    try {
        $resp = Invoke-RestMethod -Uri $url -Method POST `
            -ContentType "application/json" -Body $body
        Write-Host "`n" + $resp.candidates[0].content.parts[0].text -ForegroundColor White
    } catch {
        Write-Host "❌ Ошибка: $_" -ForegroundColor Red
    }
    return
}

Write-Host "Использование: actor-ai [-List] [-Install] [-Query 'текст']" -ForegroundColor Gray
