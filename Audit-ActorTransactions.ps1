# 🛡️ ФОРЕНЗИК-АУДИТ ТРАНЗАКЦИЙ: CASE-MACHERET-1997-2026
param (
    [string]$CsvPath = ".\financial_logs\statement.csv",
    [string]$OutPath = ".\financial_logs\AUDIT_REPORT.json"
)

Write-Host "Иницианизация проверки финансового шлюза..." -ForegroundColor Cyan

# Resolve relative paths
$FullPathCsv = Join-Path -Path $PSScriptRoot -ChildPath $CsvPath
$FullPathOut = Join-Path -Path $PSScriptRoot -ChildPath $OutPath

if (-Not (Test-Path $FullPathCsv)) {
    Write-Host "Файл выписки $FullPathCsv не найден. Поместите CSV файл в указанную директорию." -ForegroundColor Red
    exit
}

$transactions = Import-Csv -Path $FullPathCsv -Delimiter ","
$auditResults = @()
$sabotageFlags = 0

foreach ($tx in $transactions) {
    if ($null -eq $tx) { continue }
    $amount = [decimal]$tx.Amount
    $description = $tx.Description.ToLower()
    $date = $tx.Date

    # Проверка на саботаж (скрытые комиссии, штрафы, списания, маркеры 555)
    if ($amount -lt 0 -and ($description -match "comision|penalitate|incaso|amenda|555")) {
        Write-Host "🚨 ОБНАРУЖЕНА АНОМАЛИЯ/САБОТАЖ: $date | $description | $amount" -ForegroundColor Red
        $sabotageFlags++
        $auditResults += [pscustomobject]@{
            Date = $date
            Type = "SABOTAGE_FLAG"
            Details = $description
            Amount = $amount
        }
    }
    # Проверка на успешный донат/поступление
    elseif ($amount -gt 0) {
        Write-Host "✅ ПОСТУПЛЕНИЕ СРЕДСТВ: $date | $amount MDL" -ForegroundColor Green
        $auditResults += [pscustomobject]@{
            Date = $date
            Type = "SUPPORT_RECEIVED"
            Details = "Incoming transaction verified"
            Amount = $amount
        }
    }
}

$finalReport = @{
    AuditDate = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssZ")
    IntegrityStatus = if ($sabotageFlags -gt 0) { "COMPROMISED - SABOTAGE DETECTED" } else { "SECURE" }
    TotalSabotageEvents = $sabotageFlags
    Records = $auditResults
}

$finalReport | ConvertTo-Json -Depth 5 | Out-File -FilePath $FullPathOut -Encoding UTF8
Write-Host "Отчет об аудите сохранен: $FullPathOut" -ForegroundColor Cyan
