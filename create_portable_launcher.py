#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create Portable MediaCrawlerPro with Embedded Python
This creates a TRUE one-click solution - users only need Docker Desktop!
"""

import os
import subprocess
import sys
from pathlib import Path

print("=" * 70)
print("  Creating Portable MediaCrawlerPro with Embedded Python")
print("=" * 70)
print()

# Create simple launcher Python script
launcher_code = '''
import subprocess
import sys
import os
import webbrowser
import time
from pathlib import Path

def check_docker():
    """Check if Docker is running"""
    try:
        result = subprocess.run(["docker", "ps"], capture_output=True, timeout=5)
        return result.returncode == 0
    except Exception:
        return False

def main():
    print("=" * 60)
    print("   MediaCrawlerPro Launcher")
    print("=" * 60)
    print()
    
    # Check Docker
    print("[1/3] Checking Docker Desktop...")
    if not check_docker():
        print()
        print("ERROR: Docker Desktop is not running!")
        print()
        print("Please:")
        print("1. Install Docker Desktop from: https://docker.com/products/docker-desktop")
        print("2. Start Docker Desktop")
        print("3. Wait for whale icon in system tray")
        print("4. Run this program again")
        print()
        input("Press Enter to open Docker download page...")
        webbrowser.open("https://www.docker.com/products/docker-desktop")
        sys.exit(1)
    print("OK - Docker Desktop is running")
    print()
    
    # Get paths
    if getattr(sys, 'frozen', False):
        app_dir = Path(sys.executable).parent
    else:
        app_dir = Path(__file__).parent
    
    # Start Docker services
    print("[2/3] Starting Docker services...")
    os.chdir(str(app_dir))
    subprocess.run(["docker-compose", "up", "-d"], capture_output=True)
    time.sleep(3)
    print("OK - Services started")
    print()
    
    # Start Streamlit
    print("[3/3] Starting Web UI...")
    print()
    print("=" * 60)
    print("  MediaCrawlerPro is ready!")
    print("  Opening browser to: http://localhost:8501")
    print()
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
    subprocess.run([sys.executable, "-m", "streamlit", "run", "web_ui.py", 
                   "--server.port", "8501", "--server.headless", "true"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\nStopping...")
    except Exception as e:
        print(f"ERROR: {e}")
        input("Press Enter to exit...")
'''

# Write simple launcher
print("Creating simple launcher script...")
with open("simple_launcher.py", "w", encoding="utf-8") as f:
    f.write(launcher_code)

print("OK - Launcher created")
print()

# Create PyInstaller spec for the simple launcher
print("Creating executable with PyInstaller...")
print()

try:
    import PyInstaller.__main__
    
    PyInstaller.__main__.run([
        'simple_launcher.py',
        '--name=MediaCrawlerPro',
        '--onefile',
        '--console',  # Show console
        '--icon=NONE',
    ])
    
    print()
    print("=" * 70)
    print("  SUCCESS!")
    print("=" * 70)
    print()
    print("Executable created: dist/MediaCrawlerPro.exe")
    print()
    print("Next steps:")
    print("1. The EXE is standalone but needs Streamlit+dependencies")
    print("2. Users only need Docker Desktop installed")
    print("3. First run will be slow (extracting Python)")
    print()
    
except ImportError:
    print("ERROR: PyInstaller not installed")
    print("Run: pip install pyinstaller")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

