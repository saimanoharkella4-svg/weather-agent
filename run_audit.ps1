$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
# AGENT_API_TOKEN must be set in your terminal before running this script
if (-not $env:AGENT_API_TOKEN) {
    if (Test-Path ".env") {
        Get-Content ".env" | ForEach-Object {
            if ($_ -match "^\s*AGENT_API_TOKEN\s*=\s*(.*)$") {
                $env:AGENT_API_TOKEN = $matches[1].Trim()
            }
        }
    }
}

if (-not $env:AGENT_API_TOKEN) {
    Write-Error "AGENT_API_TOKEN is not set. Please set it in your terminal before running (e.g., `$env:AGENT_API_TOKEN='your_token')."
    exit 1
}

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
