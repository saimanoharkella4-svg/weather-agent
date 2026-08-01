$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
$env:AGENT_API_TOKEN = "super_secret_token_123"

Write-Host "Starting Weather Agent server on port 8082..." -ForegroundColor Cyan
$serverJob = Start-Job {
    Set-Location -Path $using:PWD
    python main.py
}

# Wait a moment for the server to start
Start-Sleep -Seconds 3

Write-Host "Running agent-audit..." -ForegroundColor Cyan
agent-audit run --target targets\agent_manifest.yaml --mode certify --variability-runs 50 --cert-output certificate.json

Write-Host "Stopping server..." -ForegroundColor Cyan
Stop-Job -Job $serverJob
Remove-Job -Job $serverJob

Write-Host "Audit Complete!" -ForegroundColor Green
