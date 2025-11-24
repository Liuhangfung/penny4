@echo off
REM MediaCrawlerPro - Complete Build and Package Script
REM This script builds the EXE and creates distribution package

echo ========================================
echo  MediaCrawlerPro Builder
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.9+ first
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Install PyInstaller
echo [STEP 1] Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller
    pause
    exit /b 1
)
echo.

REM Build EXE
echo [STEP 2] Building MediaCrawlerPro.exe...
echo This will take 5-10 minutes...
echo.
python build_exe_optimized.py
if errorlevel 1 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)
echo.

REM Create distribution package
echo [STEP 3] Creating distribution package...
echo.
python package_for_distribution.py
if errorlevel 1 (
    echo [ERROR] Packaging failed!
    pause
    exit /b 1
)
echo.

echo ========================================
echo  BUILD COMPLETE!
echo ========================================
echo.
echo Your files are ready:
echo  - dist\MediaCrawlerPro.exe
echo  - MediaCrawlerPro-Distribution\ (complete package)
echo.
echo Next steps:
echo  1. Test: Run dist\MediaCrawlerPro.exe
echo  2. Zip MediaCrawlerPro-Distribution folder
echo  3. Distribute to users!
echo.
echo Users will need Docker Desktop installed!
echo ========================================
echo.
pause

