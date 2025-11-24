@echo off
title Stop MediaCrawlerPro
echo.
echo ================================================
echo   Stopping MediaCrawlerPro
echo ================================================
echo.

echo Killing all Streamlit processes...
taskkill /F /IM streamlit.exe 2>nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *streamlit*" 2>nul
taskkill /F /IM MediaCrawlerPro*.exe 2>nul

echo.
echo Done! MediaCrawlerPro has been stopped.
echo.
pause

