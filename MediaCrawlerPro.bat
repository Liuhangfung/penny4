@echo off
REM MediaCrawlerPro Launcher Batch File
REM This is a simple alternative to the .exe - just double-click this file

echo ============================================================
echo   MediaCrawlerPro Launcher
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Docker is running
docker ps >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Docker is not running!
    echo Please start Docker Desktop first.
    echo.
    echo Press any key to continue anyway...
    pause >nul
)

REM Start Docker services
echo Starting Docker services...
docker-compose up -d

REM Wait a moment
timeout /t 5 /nobreak >nul

REM Launch web UI
echo.
echo Launching Web UI...
echo Browser will open automatically at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

python -m streamlit run web_ui.py --server.port 8501

pause

