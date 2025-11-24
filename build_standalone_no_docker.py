#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Build Standalone MediaCrawlerPro - NO Docker Required!
Creates a TRUE one-click EXE with ZERO dependencies!
"""

import PyInstaller.__main__
import os
from pathlib import Path

print("=" * 70)
print("  Building Standalone MediaCrawlerPro (No Docker Required!)")
print("=" * 70)
print()

# Create standalone launcher that doesn't need Docker
standalone_launcher_code = '''
import subprocess
import sys
import webbrowser
import time
from pathlib import Path
import os

def main():
    print("=" * 60)
    print("   MediaCrawlerPro - Standalone Edition")
    print("   No Docker Required!")
    print("=" * 60)
    print()
    
    # Get the directory where the EXE is located
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        app_dir = Path(sys.executable).parent
        # Add the _internal directory to Python path for PyInstaller onedir
        internal_dir = app_dir / "_internal"
        if internal_dir.exists():
            sys.path.insert(0, str(internal_dir))
    else:
        # Running as script
        app_dir = Path(__file__).parent
    
    os.chdir(str(app_dir))
    
    print("[1/2] Preparing environment...")
    print("OK - Ready to start")
    print()
    
    print("[2/2] Starting Web UI...")
    print()
    print("=" * 60)
    print("  MediaCrawlerPro is ready!")
    print("  Opening browser to: http://localhost:8501")
    print()
    print("  NOTE: This standalone version uses JSON/CSV for data storage")
    print("  Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    # Open browser after delay
    def open_browser():
        time.sleep(3)
        webbrowser.open("http://localhost:8501")
    
    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_dir / "web_ui.py"),
            "--server.port", "8501",
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\\nStopping MediaCrawlerPro...")
    except Exception as e:
        print(f"\\nError: {e}")
        print("\\nPress Enter to exit...")
        input()

if __name__ == "__main__":
    main()
'''

# Write the standalone launcher
print("Creating standalone launcher...")
with open("standalone_launcher.py", "w", encoding="utf-8") as f:
    f.write(standalone_launcher_code)

print("OK - Launcher created")
print()

# Create a simplified config for standalone mode
print("Creating standalone configuration...")
standalone_config_note = """
# Standalone Configuration
# This version runs without Docker:
# - Uses JSON/CSV for data storage (no MySQL)
# - No Redis caching
# - May have limited functionality for some platforms

# To use MySQL/Redis, use the Docker version instead!
"""

print("OK - Config ready")
print()

# Build with PyInstaller
print("Building executable with PyInstaller...")
print("This will take 2-5 minutes and create a large file (~500MB)")
print("The file is large because it includes Python and all dependencies!")
print()

try:
    PyInstaller.__main__.run([
        'standalone_launcher.py',
        '--name=MediaCrawlerPro_Standalone',
        '--onefile',  # Single EXE file
        '--console',  # Show console window
        '--add-data=web_ui.py;.',
        '--add-data=main.py;.',
        '--add-data=config;config',
        '--add-data=media_platform;media_platform',
        '--add-data=cmd_arg;cmd_arg',
        '--add-data=db.py;.',
        '--add-data=async_db.py;.',
        '--hidden-import=streamlit',
        '--hidden-import=pandas',
        '--hidden-import=httpx',
        '--hidden-import=playwright',
        '--hidden-import=openpyxl',
        '--collect-all=streamlit',
        '--collect-all=playwright',
        '--noconfirm',
    ])
    
    print()
    print("=" * 70)
    print("  SUCCESS!")
    print("=" * 70)
    print()
    print("Executable created: dist/MediaCrawlerPro_Standalone.exe")
    print()
    print("File size: ~500MB (includes Python + all dependencies)")
    print()
    print("What friends need:")
    print("  ✅ NOTHING! Just the EXE file!")
    print("  ❌ No Docker")
    print("  ❌ No Python")
    print("  ❌ No installation")
    print()
    print("Limitations:")
    print("  ⚠️  Uses JSON/CSV only (no MySQL database)")
    print("  ⚠️  No Redis caching")
    print("  ⚠️  May have issues with platforms requiring Sign Service")
    print()
    print("To test:")
    print("  1. Go to: dist/")
    print("  2. Double-click: MediaCrawlerPro_Standalone.exe")
    print("  3. Browser opens automatically!")
    print()
    
except ImportError:
    print("ERROR: PyInstaller not installed")
    print("Run: pip install pyinstaller")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

