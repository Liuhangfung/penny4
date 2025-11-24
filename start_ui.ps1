# MediaCrawlerPro Web UI Startup Script

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "    MediaCrawlerPro Web UI" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Set UTF-8 encoding
$env:PYTHONIOENCODING = "utf-8"

# Get the script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "Starting Streamlit server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Once the server starts, open your browser to:" -ForegroundColor Green
Write-Host "  http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start streamlit
streamlit run web_ui.py

Write-Host ""
Write-Host "Server stopped." -ForegroundColor Red


