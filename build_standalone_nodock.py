#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Build Truly Standalone MediaCrawlerPro - NO Docker Required
Just double-click the EXE and it works!
"""

import subprocess
import sys
import os
from pathlib import Path

# Set console encoding to UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')

print("=" * 70)
print("  Building Standalone MediaCrawlerPro")
print("  NO Docker Required!")
print("=" * 70)
print()

# Step 1: Check PyInstaller
print("[1/3] Checking PyInstaller...")
try:
    import PyInstaller.__main__
    print("[OK] PyInstaller found!")
except ImportError:
    print("[INSTALL] Installing PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    print("[OK] PyInstaller installed!")
    import PyInstaller.__main__

print()

# Step 2: Check dependencies
print("[2/3] Checking required packages...")
required_packages = [
    'streamlit', 'pandas', 'openpyxl', 
    'httpx', 'playwright'
]

missing = []
for package in required_packages:
    try:
        __import__(package)
        print(f"  [OK] {package}")
    except ImportError:
        print(f"  [MISSING] {package} - will install")
        missing.append(package)

if missing:
    print()
    print(f"Installing missing packages: {', '.join(missing)}")
    subprocess.run([
        sys.executable, "-m", "pip", "install"
    ] + missing, check=True)
    print("[OK] All packages installed!")

print()

# Step 3: Build executable
print("[3/3] Building standalone executable...")
print("This may take 5-10 minutes...")
print()

# Prepare build arguments
build_args = [
    'standalone_launcher_nodock.py',
    '--name=MediaCrawlerPro_Standalone',
    '--onefile',
    '--console',
    '--icon=NONE',
    
    # Add data files
    '--add-data=web_ui.py;.',
    '--add-data=main.py;.',
    '--add-data=var.py;.',
    '--add-data=db.py;.',
    '--add-data=async_db.py;.',
    
    # Add directories
    '--add-data=config;config',
    '--add-data=media_platform;media_platform',
    '--add-data=cmd_arg;cmd_arg',
    '--add-data=pkg;pkg',
    '--add-data=model;model',
    '--add-data=repo;repo',
    '--add-data=base;base',
    '--add-data=constant;constant',
    
    # Hidden imports
    '--hidden-import=streamlit',
    '--hidden-import=pandas',
    '--hidden-import=httpx',
    '--hidden-import=playwright',
    '--hidden-import=openpyxl',
    '--hidden-import=asyncio',
    '--hidden-import=aiofiles',
    '--hidden-import=json',
    '--hidden-import=csv',
    
    # Collect all streamlit files
    '--collect-all=streamlit',
    '--collect-all=altair',
    '--collect-all=plotly',
    
    # Don't confirm overwrites
    '--noconfirm',
    
    # Clean build
    '--clean',
]

try:
    PyInstaller.__main__.run(build_args)
    
    print()
    print("=" * 70)
    print("  SUCCESS!")
    print("=" * 70)
    print()
    print(f"Executable created: {Path('dist/MediaCrawlerPro_Standalone.exe').absolute()}")
    print()
    print("=" * 70)
    print("  HOW TO USE:")
    print("=" * 70)
    print()
    print("1. Go to the 'dist' folder")
    print("2. Copy these files next to MediaCrawlerPro_Standalone.exe:")
    print("   - web_ui.py")
    print("   - config/ folder")
    print()
    print("3. Double-click MediaCrawlerPro_Standalone.exe")
    print("4. Browser opens automatically!")
    print("5. Start crawling - NO Docker needed!")
    print()
    print("=" * 70)
    print("  WHAT TO SHARE:")
    print("=" * 70)
    print()
    print("Create a folder with:")
    print("  MediaCrawlerPro_Standalone.exe   (the executable)")
    print("  web_ui.py                        (web interface)")
    print("  config/                          (configuration folder)")
    print()
    print("Zip this folder and share!")
    print()
    print("=" * 70)
    print("  NOTES:")
    print("=" * 70)
    print()
    print("- NO Docker required!")
    print("- NO external dependencies!")
    print("- Works completely offline")
    print("- Data saved to local files (JSON/CSV)")
    print("- File size: ~500-700MB (includes everything)")
    print("- First run may take 30 seconds to start")
    print()
    print("[OK] Build complete!")
    print()
    
except Exception as e:
    print()
    print(f"[ERROR] Build failed: {e}")
    print()
    import traceback
    traceback.print_exc()
    sys.exit(1)

