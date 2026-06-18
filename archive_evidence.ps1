$EvidenceFile = ".\audits\dual_run_comparative_audit.json"
$VaultPath = "H:\ACTOR_EVIDENCE_VAULT"
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

if (Test-Path $EvidenceFile) {
    $Hash = (Get-FileHash $EvidenceFile -Algorithm SHA256).Hash
    $Manifest = [PSCustomObject]@{
        Timestamp = $Timestamp
        OriginalFile = "dual_run_comparative_audit.json"
        SHA256 = $Hash
        Author = "A©tor"
    }
    
    $ManifestJson = $Manifest | ConvertTo-Json
    $ManifestJson | Out-File "$VaultPath\manifest_$Timestamp.json" -Encoding utf8
    
    Copy-Item $EvidenceFile "$VaultPath\reports\audit_$Timestamp.json"
    
    Push-Location $VaultPath
    git add .
    git commit -m "TI-ULA Evidence Vault: Audit $Timestamp [SHA256: $Hash]"
    git push origin main
    Pop-Location
    
    Write-Host "✅ Доказательства зафиксированы в Vault. SHA256: $Hash" -ForegroundColor Green
} else {
    Write-Host "❌ Файл отчета не найден!" -ForegroundColor Red
}
