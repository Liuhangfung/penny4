@echo off
chcp 65001 > nul
REM ============================================================
REM MediaCrawlerPro - One-Click Launcher
REM For your friends - just double-click to run!
REM ============================================================

REM Change to the directory where this BAT file is located
cd /d "%~dp0"

title MediaCrawlerPro

echo.
echo ============================================================
echo            🕷️  MediaCrawlerPro Launcher
echo ============================================================
echo.

REM ============================================================
REM STEP 1: Check Docker Desktop
REM ============================================================
echo [1/3] Checking Docker Desktop...
docker ps >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ Docker Desktop is not running!
    echo.
    echo ⚠️  REQUIRED: Please install and start Docker Desktop
    echo.
    echo 📥 Download from: https://www.docker.com/products/docker-desktop
    echo.
    echo After installing:
    echo   1. Start Docker Desktop
    echo   2. Wait for the whale icon to appear in system tray
    echo   3. Run this file again
    echo.
    start https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo ✅ Docker Desktop is running
echo.

REM ============================================================  
REM STEP 2: Start Docker Services
REM ============================================================
echo [2/3] Starting services...
docker-compose up -d >nul 2>&1
timeout /t 3 /nobreak >nul
echo ✅ Services started
echo.

REM ============================================================
REM STEP 3: Check Python and Start Web UI
REM ============================================================
echo [3/3] Starting Web UI...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ Python not found!
    echo.
    echo ⚠️  REQUIRED: Please install Python 3.9 or newer
    echo.
    echo 📥 Download from: https://www.python.org/downloads/
    echo.
    echo ⚠️  IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Auto-install dependencies if needed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo.
    echo 📦 Installing dependencies ^(first time only, please wait...^)
    pip install -q streamlit pandas openpyxl pymysql httpx
    echo ✅ Dependencies installed
    echo.
)

REM Start Web UI
echo.
echo ============================================================
echo  ✅ MediaCrawlerPro is ready!
echo.
echo  🌐 Opening browser in 3 seconds...
echo  📍 URL: http://localhost:8501
echo.
echo  ⏹️  Press Ctrl+C to stop
echo ============================================================
echo.

REM Open browser after delay
start /B cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:8501"

REM Start Streamlit
python -m streamlit run web_ui.py --server.port 8501 --server.headless true 2>nul

REM If Streamlit exits, pause so user can see any errors
pause

