#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to create executable for MediaCrawlerPro Web UI
Run: python create_exe.py
"""

import subprocess
import sys
import os
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    print("Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("✅ PyInstaller installed!")

def create_exe():
    """Create executable using PyInstaller"""
    print("🔨 Creating executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=MediaCrawlerPro",
        "--onefile",
        "--windowed",  # No console window
        "--icon=NONE",  # You can add an icon file later
        "--add-data=config;config",  # Include config directory
        "--hidden-import=streamlit",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--hidden-import=pymysql",
        "--hidden-import=httpx",
        "--hidden-import=pkg_resources.py2_warn",
        "--collect-all=streamlit",
        "--collect-all=altair",
        "web_ui.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n✅ Executable created successfully!")
        print("📁 Location: dist/MediaCrawlerPro.exe")
        print("\n⚠️  Note: Docker Desktop must be installed separately")
        print("   Users need to install Docker Desktop before running the exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating executable: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("MediaCrawlerPro - Executable Creator")
    print("=" * 60)
    
    if not check_pyinstaller():
        print("PyInstaller not found. Installing...")
        install_pyinstaller()
    
    create_exe()

