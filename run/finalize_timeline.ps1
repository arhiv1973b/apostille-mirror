
$finalEvents = New-Object System.Collections.Generic.List[PSObject]
$finalEvents.Add([PSCustomObject]@{ Timestamp = "2026-06-15T19:00:00Z"; Type = "IDENTITY_AUDIT_COMPLETE"; Detail = "Mapped Trandafilova-Chirca link. Identified fictitious marriage as fraud mechanism."; Source = "IDENTITY_FRAUD_REPORT_20260615.json" })
$finalEvents.Add([PSCustomObject]@{ Timestamp = "2026-06-15T19:30:00Z"; Type = "EVIDENCE_INDEXING"; Detail = "Indexed 'Суд мед экспертиза_1.pdf' and '25M lei' set. Verified identical hashes for asset set."; Source = "H:\Загрузки" })
$finalEvents.Add([PSCustomObject]@{ Timestamp = "2026-06-15T20:00:00Z"; Type = "DISPATCH_READY"; Detail = "Finalized INTERNATIONAL_SUBMISSION_PACKAGE. Ready for Phase II."; Source = "Gemini CLI" })

$timelinePath = "apostille-mirror\FORENSIC_TIMELINE_20260615.json"
if (Test-Path $timelinePath) {
    $timeline = Get-Content $timelinePath -Raw | ConvertFrom-Json
    foreach ($event in $finalEvents) {
        $timeline += $event
    }
    $timeline | ConvertTo-Json -Depth 5 | Out-File $timelinePath -Encoding UTF8
    Write-Host "Timeline finalized: $timelinePath"
}
