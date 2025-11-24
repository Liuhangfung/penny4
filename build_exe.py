# MediaCrawlerPro Executable Builder
# This script creates a standalone executable

import PyInstaller.__main__
import os
import sys
from pathlib import Path

print("=" * 60)
print("🕷️  MediaCrawlerPro Executable Builder")
print("=" * 60)
print()
print("📦 Starting PyInstaller build process...")
print("   This may take 5-15 minutes depending on your system.")
print("   Please be patient...")
print()

try:
    # PyInstaller configuration
    PyInstaller.__main__.run([
        'launcher.py',
        '--name=MediaCrawlerPro',
        '--onefile',
        '--console',  # Changed to console so we can see progress
        '--icon=NONE',
        '--add-data=config;config',
        '--add-data=web_ui.py;.',
        '--hidden-import=streamlit',
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
        '--hidden-import=pymysql',
        '--hidden-import=httpx',
        '--hidden-import=pkg_resources.py2_warn',
        '--collect-all=streamlit',
        '--collect-all=altair',
    ])
    
    # Check if build succeeded
    exe_path = Path("dist") / "MediaCrawlerPro.exe"
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print()
        print("=" * 60)
        print("✅ Build completed successfully!")
        print("=" * 60)
        print(f"📁 Executable location: {exe_path.absolute()}")
        print(f"📊 Executable size: {size_mb:.2f} MB")
        print()
        print("🚀 You can now run MediaCrawlerPro.exe to start the application!")
        print("=" * 60)
    else:
        print()
        print("⚠️  Build completed but executable not found at expected location.")
        print("   Check the 'dist' directory for output files.")
        
except Exception as e:
    print()
    print("=" * 60)
    print("❌ Build failed with error:")
    print("=" * 60)
    print(str(e))
    print()
    print("💡 Troubleshooting:")
    print("   1. Make sure all dependencies are installed: pip install -r requirements.txt")
    print("   2. Try running with --console flag to see detailed errors")
    print("   3. Check if antivirus is blocking PyInstaller")
    sys.exit(1)

