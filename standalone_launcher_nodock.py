#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MediaCrawlerPro - Truly Standalone Launcher
NO Docker Required - Everything Works Locally
"""

import subprocess
import sys
import webbrowser
import time
from pathlib import Path
import os
import threading

def main():
    print("=" * 70)
    print("           MediaCrawlerPro - Standalone Edition")
    print("           NO Docker Required!")
    print("=" * 70)
    print()
    
    # Get the directory where the EXE is located
    if getattr(sys, 'frozen', False):
        app_dir = Path(sys.executable).parent
        # Add PyInstaller's internal directory to path
        if hasattr(sys, '_MEIPASS'):
            sys.path.insert(0, sys._MEIPASS)
    else:
        app_dir = Path(__file__).parent
    
    os.chdir(str(app_dir))
    
    print("[1/2] Setting up environment...")
    
    # Set environment to use local storage (no Docker)
    os.environ['USE_DOCKER'] = 'false'
    os.environ['ENABLE_IP_PROXY'] = '0'
    os.environ['ENABLE_SIGN_SERVICE'] = '0'
    
    print("✅ Using local storage (JSON/CSV files)")
    print("✅ No Docker required")
    print()
    
    print("[2/2] Starting Web Interface...")
    print()
    print("=" * 70)
    print("  ✅ MediaCrawlerPro is ready!")
    print("  🌐 Opening browser to: http://localhost:8501")
    print()
    print("  Mode: Standalone (No Docker)")
    print("  Storage: Local files in 'data/' folder")
    print()
    print("  Press Ctrl+C to stop")
    print("=" * 70)
    print()
    
    # Open browser after delay
    def open_browser():
        time.sleep(4)
        try:
            webbrowser.open("http://localhost:8501")
        except:
            pass
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Find web_ui.py
    web_ui_path = app_dir / "web_ui.py"
    
    if not web_ui_path.exists():
        print(f"❌ ERROR: web_ui.py not found at {web_ui_path}")
        print("\nMake sure web_ui.py is in the same folder as this executable.")
        input("\nPress Enter to exit...")
        return
    
    # Run streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(web_ui_path),
            "--server.port", "8501",
            "--server.headless", "true",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n\nStopping MediaCrawlerPro...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all files are in the same folder")
        print("2. Try running as administrator")
        print("3. Check if port 8501 is already in use")
        print("\nPress Enter to exit...")
        input()

if __name__ == "__main__":
    main()

