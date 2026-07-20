
$newEvents = New-Object System.Collections.Generic.List[PSObject]
$newEvents.Add([PSCustomObject]@{ Timestamp = "2026-06-15T10:00:00Z"; Type = "DICOM_AUDIT"; Detail = "Verified 1180+ slices in Audit Data Frame. Confirmed missing Coronal views."; Source = "audit_data_frame_20260613.csv" })
$newEvents.Add([PSCustomObject]@{ Timestamp = "2026-06-15T11:30:00Z"; Type = "IDENTITY_FRAUD_DETECTED"; Detail = "Confirmed Trandafilova-Chirca link and Andrei Vacarciuc role."; Source = "инспекторат.pdf_translated.txt" })
$newEvents.Add([PSCustomObject]@{ Timestamp = "2026-06-15T15:00:00Z"; Type = "HASH_VERIFICATION"; Detail = "Verified core evidence: HOMICIDE.pdf (E9EB...) and 25M_LEI.jpg (C2D1...)."; Source = "verify_integrity.ps1" })
$newEvents.Add([PSCustomObject]@{ Timestamp = "2026-06-15T18:00:00Z"; Type = "MANIFEST_GENERATION"; Detail = "Generated FINAL_AUDIT_MANIFEST_20260615.json and International Submission Package."; Source = "Gemini CLI" })

$timelinePath = "apostille-mirror\FORENSIC_TIMELINE_20260611.json"
$newTimelinePath = "apostille-mirror\FORENSIC_TIMELINE_20260615.json"

if (Test-Path $timelinePath) {
    $timeline = Get-Content $timelinePath -Raw | ConvertFrom-Json
    foreach ($event in $newEvents) {
        $timeline += $event
    }
    $timeline | ConvertTo-Json -Depth 5 | Out-File $newTimelinePath -Encoding UTF8
    Write-Host "Updated timeline saved to $newTimelinePath"
} else {
    $newEvents | ConvertTo-Json -Depth 5 | Out-File $newTimelinePath -Encoding UTF8
    Write-Host "New timeline created at $newTimelinePath"
}
