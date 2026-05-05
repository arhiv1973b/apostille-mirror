function atask {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true, Position=0)][string]$Title,
        [Parameter(Position=1)][string]$Body = "",
        [Parameter()][string[]]$Labels = @(),
        [Parameter()][string]$Repo = "arhiv1973b/apostille-mirror",
        [Parameter()][switch]$Dry
    )

    # 1. Загрузка токена из Vault (уже 8 ключей в реестре)
    $token = $null
    try { $token = Load-Secret "GITHUB_TOKEN" } catch {}
    if (-not $token) { $token = $env:GITHUB_TOKEN }
    
    if (-not $token) {
        Write-Host "❌ GITHUB_TOKEN не найден. Добавьте его в Vault." -ForegroundColor Red
        return
    }

    # 2. Формирование тела с подписью A©tor
    $ts = (Get-Date -Format "yyyy-MM-dd HH:mm:ss UTC")
    $tag = "A©TOR · CASE-MACHERET-1997-2026 · $ts"
    $full_body = if ($Body) { "$Body`n`n---`n$tag" } else { $tag }

    # 3. Подготовка JSON
    $payloadObj = @{ title=$Title; body=$full_body }
    if ($Labels.Count -gt 0) { $payloadObj.labels = $Labels }
    $payloadJson = $payloadObj | ConvertTo-Json -Depth 5

    if ($Dry) {
        Write-Host "`n🔍 [DRY RUN] Repo: $Repo | Title: $Title" -ForegroundColor Cyan
        Write-Host $full_body -ForegroundColor DarkGray
        return
    }

    # 4. Отправка через байтовый массив (решение ошибки 400 для PS 5.1)
    try {
        $url = "https://api.github.com/repos/$Repo/issues"
        $headers = @{ 
            Authorization = "Bearer $token"
            Accept = "application/vnd.github+json"
            "X-GitHub-Api-Version" = "2022-11-28"
        }
        
        $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($payloadJson)
        
        $r = Invoke-RestMethod -Uri $url -Method POST -Headers $headers `
                               -Body $utf8Bytes -ContentType "application/json; charset=utf-8"
        
        Write-Host "`n✅ Issue #$($r.number) создан успешно!" -ForegroundColor Green
        Write-Host "🔗 URL: $($r.html_url)" -ForegroundColor Cyan
    } catch {
        Write-Host "`n❌ GitHub API Error: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.Exception.Response) {
            $reader = [System.IO.StreamReader]::new($_.Exception.Response.GetResponseStream())
            Write-Host "Детали: $($reader.ReadToEnd())" -ForegroundColor Gray
        }
    }
}
