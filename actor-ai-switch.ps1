param(
    [string]$Model = "",
    [string]$Prompt = "",
    [switch]$List,
    [switch]$Install,
    [switch]$Interactive
)

function Write-Color($text, $color="White") { Write-Host $text -ForegroundColor $color }

function Write-Header {
    Write-Host ""
    Write-Color "╔══════════════════════════════════════════════════════╗" Cyan
    Write-Color "║      A©tor AI SWITCHER v2.1 — UTF-8 EDITION          ║" Cyan
    Write-Color "║         CASE-MACHERET-1997-2026 · Active             ║" Cyan
    Write-Color "╚══════════════════════════════════════════════════════╝" Cyan
    Write-Host ""
}

$MODELS = [ordered]@{
    "gemini-flash"   = @{ Provider="gemini";     EnvKey="GOOGLE_GENERATIVE_AI_API_KEY"; Name="Gemini 2.5 Flash";        ID="gemini-2.5-flash" }
    "gemini-3-flash" = @{ Provider="gemini";     EnvKey="GOOGLE_GENERATIVE_AI_API_KEY"; Name="Gemini 3 Flash Preview"; ID="gemini-3-flash-preview" }
    "claude-sonnet"  = @{ Provider="anthropic";  EnvKey="ANTHROPIC_API_KEY";            Name="Claude Sonnet 4.6";      ID="claude-sonnet-4-6" }
    "gpt-4o"         = @{ Provider="openai";     EnvKey="OPENAI_API_KEY";               Name="GPT-4o";                  ID="gpt-4o" }
    "grok"           = @{ Provider="grok";       EnvKey="GROK_API_KEY";                 Name="Grok (xAI)";              ID="grok-3-mini" }
}

function Invoke-AI {
    param([string]$Alias, [string]$UserPrompt)
    $cfg = $MODELS[$Alias]
    $apiKey = [System.Environment]::GetEnvironmentVariable($cfg.EnvKey)
    if (-not $apiKey) { Write-Color "❌ Ключ $($cfg.EnvKey) не найден." Red; return }

    Write-Color "`n  🤖 [$($cfg.Name)] обрабатывает запрос..." Yellow

    $headers = @{ "Content-Type" = "application/json" }
    $uri = ""; $jsonBody = ""

    if ($cfg.Provider -eq "gemini") {
        $uri = "https://generativelanguage.googleapis.com/v1beta/models/$($cfg.ID):generateContent?key=$apiKey"
        $jsonBody = @{ contents = @(@{ parts = @(@{ text = $UserPrompt }) }) } | ConvertTo-Json -Depth 5
    } elseif ($cfg.Provider -eq "anthropic") {
        $uri = "https://api.anthropic.com/v1/messages"
        $headers["x-api-key"] = $apiKey
        $headers["anthropic-version"] = "2023-06-01"
        $jsonBody = @{ model=$cfg.ID; max_tokens=1024; messages=@(@{ role="user"; content=$UserPrompt }) } | ConvertTo-Json -Depth 5
    } else {
        $uri = if ($cfg.Provider -eq "openai") { "https://api.openai.com/v1/chat/completions" } else { "https://api.x.ai/v1/chat/completions" }
        $headers["Authorization"] = "Bearer $apiKey"
        $jsonBody = @{ model=$cfg.ID; messages=@(@{ role="user"; content=$UserPrompt }) } | ConvertTo-Json -Depth 5
    }

    # КРИТИЧЕСКИЙ ФИКС КОДИРОВКИ
    $postData = [System.Text.Encoding]::UTF8.GetBytes($jsonBody)

    try {
        $resp = Invoke-RestMethod -Uri $uri -Method POST -Headers $headers -Body $postData -TimeoutSec 60
        $text = if ($cfg.Provider -eq "gemini") { $resp.candidates[0].content.parts[0].text } 
                elseif ($cfg.Provider -eq "anthropic") { $resp.content[0].text } 
                else { $resp.choices[0].message.content }
        
        Write-Color "─────────────────────────────────────────────────" DarkGray
        Write-Color "  [$($cfg.Name)]" Cyan
        Write-Color "─────────────────────────────────────────────────" DarkGray
        Write-Host $text
        Write-Color "─────────────────────────────────────────────────" DarkGray
    } catch { Write-Color "❌ Ошибка: $($_.Exception.Message)" Red }
}

if ($List) { $MODELS.Keys | ForEach-Object { Write-Color "  [$_]" Green } }
elseif ($Interactive) {
    Write-Header
    $current = "gemini-3-flash"
    while ($true) {
        $input = Read-Host "  A©tor [$current]> "
        if ($input -eq "/exit") { break }
        if ($input.Trim() -ne "") { Invoke-AI -Alias $current -UserPrompt $input }
    }
}
elseif ($Model -ne "" -and $Prompt -ne "") { Invoke-AI -Alias $Model -UserPrompt $Prompt }
else { Write-Header; Write-Color "Использование: actor-ai -Interactive" Yellow }
