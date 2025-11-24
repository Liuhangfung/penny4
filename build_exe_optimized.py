# MediaCrawlerPro Executable Builder (Optimized)
# This script creates a standalone executable with exclusions to reduce size

import PyInstaller.__main__
import os
import sys

# Exclude unnecessary large packages to reduce executable size
excludes = [
    'torch',           # Not needed for web UI
    'torchvision',     # Not needed
    'torchaudio',     # Not needed
    'tensorflow',     # Not needed
    'sklearn',        # Not needed
    'transformers',   # Not needed
    'scipy',          # Not needed (unless pandas requires it)
    'matplotlib',      # Not needed for web UI
    'plotly',         # Not needed (Streamlit uses its own)
    'jupyter',        # Not needed
    'notebook',       # Not needed
    'IPython',        # Not needed
    'pytest',         # Not needed
    'pytz',           # Can be excluded if not using timezones
]

# PyInstaller configuration
PyInstaller.__main__.run([
    'launcher.py',
    '--name=MediaCrawlerPro',
    '--onefile',
    '--console',  # Show console window (needed for user feedback)
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
    '--exclude-module=torch',
    '--exclude-module=torchvision',
    '--exclude-module=torchaudio',
    '--exclude-module=tensorflow',
    '--exclude-module=sklearn',
    '--exclude-module=transformers',
    '--exclude-module=scipy',
    '--exclude-module=matplotlib',
    '--exclude-module=plotly',
    '--exclude-module=jupyter',
    '--exclude-module=notebook',
    '--exclude-module=IPython',
    '--exclude-module=pytest',
])

print("\n" + "="*60)
print("✅ Build complete!")
print("📁 Executable location: dist/MediaCrawlerPro.exe")
print("="*60)

