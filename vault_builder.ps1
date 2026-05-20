# vault_builder.ps1
$SourceDir = "C:\Users\arhiv\ACTOR_DEV_ENV\apostille-mirror"
$DistDir   = "C:\Users\arhiv\ACTOR_DEV_ENV\dist"
$Manifest  = Join-Path $DistDir "index.json"
$Map = @{}

if (!(Test-Path $DistDir)) { New-Item -ItemType Directory -Path $DistDir }

$Files = Get-ChildItem -Path $SourceDir -Filter *.md -Recurse

foreach ($File in $Files) {
    $Content = Get-Content $File.FullName -Raw
    
    # Верификация: только файлы с маркером A©tor или A©t0r
    if ($Content -match "A©tor" -or $Content -match "A©t0r") {
        
        # Генерация хэша для имени файла
        $Hash = (Get-FileHash $File.FullName -Algorithm SHA256).Hash.Substring(0, 16)
        $HtmlName = "$Hash.html"
        $HtmlPath = Join-Path $DistDir $HtmlName
        
        # Обновление маппинга
        $Map[$Hash] = $File.Name
        
        # Сборка HTML
        $Header = "<html><head><meta charset='utf-8'></head><body>"
        $Footer = "<footer>CASE-MACHERET-1997-2026. Вектор: Jus Cogens & Erga Omnes. Подтверждено: A©tor.</footer></body></html>"
        $FullHtml = $Header + ($Content | ConvertFrom-Markdown | Select-Object -ExpandProperty Html) + $Footer
        
        $FullHtml | Out-File $HtmlPath -Encoding utf8
        Write-Output "✅ [TRUSTED] Собрано: $($File.Name) -> $HtmlName"
    }
}

# Сохранение маппинга для восстановления имен
$Map | ConvertTo-Json | Out-File $Manifest -Encoding utf8
