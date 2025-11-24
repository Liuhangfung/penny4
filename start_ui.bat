@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo Starting MediaCrawlerPro Web UI...
echo.
echo Once started, open your browser to:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.
set PYTHONIOENCODING=utf-8
streamlit run web_ui.py
pause


