
$cutOffDate = Get-Date "2026-06-14"
$baseDir = "H:\ACTOR_DEV_ENV\apostille-mirror"

Get-ChildItem -Path $baseDir -Recurse | Where-Object { $_.LastWriteTime -ge $cutOffDate } | Select-Object FullName, LastWriteTime | Format-Table -AutoSize
