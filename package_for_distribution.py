#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Package MediaCrawlerPro for distribution
Creates a folder with everything users need
"""

import shutil
import os
from pathlib import Path

def create_distribution_package():
    """Create distribution package"""
    
    print("=" * 60)
    print("📦 Creating MediaCrawlerPro Distribution Package")
    print("=" * 60)
    print()
    
    # Define paths
    project_dir = Path(__file__).parent
    dist_exe = project_dir / "dist" / "MediaCrawlerPro.exe"
    package_dir = project_dir / "MediaCrawlerPro-Distribution"
    
    # Check if EXE exists
    if not dist_exe.exists():
        print("❌ Error: MediaCrawlerPro.exe not found!")
        print("   Please run 'python build_exe_optimized.py' first")
        return False
    
    # Create package directory
    print("📁 Creating distribution folder...")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(exist_ok=True)
    
    # Copy executable
    print("📋 Copying MediaCrawlerPro.exe...")
    shutil.copy2(dist_exe, package_dir / "MediaCrawlerPro.exe")
    
    # Copy essential files
    essential_files = [
        "docker-compose.yaml",
        "Dockerfile",
        "USER_README.txt",
        "requirements.txt",
        "web_ui.py",
        "main.py",
        "db.py",
        "async_db.py",
        "var.py",
    ]
    
    print("📋 Copying essential files...")
    for file in essential_files:
        src = project_dir / file
        if src.exists():
            shutil.copy2(src, package_dir / file)
            print(f"   ✓ {file}")
    
    # Copy directories
    directories_to_copy = [
        "config",
        "base",
        "cmd_arg",
        "constant",
        "media_platform",
        "model",
        "pkg",
        "repo",
        "schema",
    ]
    
    print("📋 Copying directories...")
    for dir_name in directories_to_copy:
        src_dir = project_dir / dir_name
        dst_dir = package_dir / dir_name
        if src_dir.exists():
            shutil.copytree(src_dir, dst_dir, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo'))
            print(f"   ✓ {dir_name}/")
    
    # Create empty data directory
    (package_dir / "data").mkdir(exist_ok=True)
    print("   ✓ data/ (empty)")
    
    # Create Quick Start guide
    print("📝 Creating QUICK_START.txt...")
    quick_start = package_dir / "QUICK_START.txt"
    with open(quick_start, 'w', encoding='utf-8') as f:
        f.write("""
========================================
   MediaCrawlerPro - QUICK START
========================================

REQUIREMENTS:
1. Windows 10/11
2. Docker Desktop (MUST BE INSTALLED!)
   Download: https://www.docker.com/products/docker-desktop

STEPS TO USE:
1. Install Docker Desktop (if not already installed)
2. Start Docker Desktop (look for whale icon in system tray)
3. Double-click MediaCrawlerPro.exe
4. Browser will open automatically to http://localhost:8501
5. Configure your account cookies
6. Start crawling!

For detailed instructions, see USER_README.txt

========================================
   ENJOY! 🎉
========================================
""")
    
    # Create distribution info
    print("📝 Creating DISTRIBUTION_INFO.txt...")
    info_file = package_dir / "DISTRIBUTION_INFO.txt"
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write("""
MediaCrawlerPro Distribution Package
=====================================

This package contains:
- MediaCrawlerPro.exe (main executable)
- config/ (configuration files)
- All necessary Python modules
- Docker configuration files
- User documentation

What users need:
1. Windows 10/11 (64-bit)
2. Docker Desktop installed and running
3. 4GB RAM minimum (8GB recommended)
4. 5GB free disk space

Users do NOT need:
- Python installation
- Manual dependency installation
- Server setup

Everything runs locally on their computer!

=====================================
For support: GitHub repository
Educational purposes only!
=====================================
""")
    
    # Calculate package size
    total_size = sum(
        f.stat().st_size 
        for f in package_dir.rglob('*') 
        if f.is_file()
    )
    size_mb = total_size / (1024 * 1024)
    
    print()
    print("=" * 60)
    print("✅ Distribution package created successfully!")
    print("=" * 60)
    print(f"📁 Location: {package_dir}")
    print(f"📊 Total size: {size_mb:.1f} MB")
    print()
    print("📦 Package contents:")
    print(f"   - MediaCrawlerPro.exe (ready to distribute)")
    print(f"   - All necessary files and configurations")
    print(f"   - User documentation")
    print()
    print("📤 Next steps:")
    print("   1. Test the package on a clean Windows machine")
    print("   2. Create a ZIP file of the distribution folder")
    print("   3. Distribute to users!")
    print()
    print("⚠️  Users will need Docker Desktop installed!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = create_distribution_package()
        if not success:
            input("\nPress Enter to exit...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")

