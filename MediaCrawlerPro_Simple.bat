@echo off
chcp 65001 > nul
REM MediaCrawlerPro - Simple One-Click Launcher
REM Just double-click this file to run!

echo.
echo ============================================================
echo            MediaCrawlerPro Launcher
echo ============================================================
echo.

REM Check if Docker Desktop is running
docker ps >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Desktop is not running!
    echo.
    echo Please:
    echo 1. Install Docker Desktop from: https://www.docker.com/products/docker-desktop
    echo 2. Start Docker Desktop
    echo 3. Wait for it to fully start ^(whale icon in system tray^)
    echo 4. Run this file again
    echo.
    pause
    exit /b 1
)

echo [OK] Docker Desktop is running
echo.

REM Start Docker services
echo [STEP 1] Starting Docker services...
docker-compose up -d 2>nul
if errorlevel 1 (
    echo [WARNING] Docker services may already be running
) else (
    echo [OK] Docker services started
)
echo.

REM Wait for services to be ready
echo [STEP 2] Waiting for services to start...
timeout /t 5 /nobreak >nul
echo [OK] Services ready
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Python not found - installing requirements...
    echo.
    echo [ERROR] Python is required but not installed!
    echo.
    echo Please install Python 3.9+ from: https://www.python.org/
    echo Then run this file again.
    echo.
    pause
    exit /b 1
)

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlength 1 (
    echo [STEP 3] Installing Streamlit ^(first time only^)...
    pip install streamlit pandas openpyxl pymysql httpx -q
    echo [OK] Streamlit installed
)

REM Start Web UI
echo [STEP 3] Starting Web UI...
echo.
echo ============================================================
echo  MediaCrawlerPro is starting!
echo.
echo  Web UI will open at: http://localhost:8501
echo.
echo  Press Ctrl+C to stop
echo ============================================================
echo.

REM Wait 3 seconds then open browser
start /B timeout /t 3 /nobreak >nul && start http://localhost:8501

REM Start Streamlit
python -m streamlit run web_ui.py --server.port 8501 --server.headless true

pause

