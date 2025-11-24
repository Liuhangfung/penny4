# MediaCrawlerPro Executable Build Guide

## Overview
This guide explains how to create a standalone executable (.exe) file for MediaCrawlerPro that users can double-click to run.

## Prerequisites

### For Building the EXE:
1. Python 3.9+ installed
2. PyInstaller: `pip install pyinstaller`
3. All project dependencies installed

### For End Users:
1. **Docker Desktop must be installed** (required!)
   - Download: https://www.docker.com/products/docker-desktop
   - Users must install Docker Desktop separately
2. Windows 10/11

## Building the Executable

### Option 1: Using the Build Script (Recommended)

```powershell
# Install PyInstaller if not already installed
pip install pyinstaller

# Run the build script
python build_exe.py
```

### Option 2: Manual PyInstaller Command

```powershell
pyinstaller --name=MediaCrawlerPro --onefile --windowed --add-data="config;config" --add-data="web_ui.py;." --hidden-import=streamlit --hidden-import=pandas --hidden-import=openpyxl --hidden-import=pymysql --hidden-import=httpx --collect-all=streamlit launcher.py
```

### Option 3: Using the Spec File

```powershell
pyinstaller MediaCrawlerPro.spec
```

## Output Location

After building, the executable will be in:
- **dist/MediaCrawlerPro.exe** (onefile mode)
- OR **dist/MediaCrawlerPro/** folder (onedir mode)

## Distribution Package

When distributing to users, include:

1. **MediaCrawlerPro.exe** (the executable)
2. **config/** folder (if not bundled)
3. **README.txt** with instructions:
   ```
   MediaCrawlerPro Installation Instructions
   
   1. Install Docker Desktop:
      Download from: https://www.docker.com/products/docker-desktop
      
   2. Start Docker Desktop
   
   3. Double-click MediaCrawlerPro.exe
   
   4. The web browser will open automatically
      If not, go to: http://localhost:8501
   
   5. Configure your account cookies in the UI
   
   6. Start crawling!
   ```

## Important Notes

### Limitations:
- **Docker Desktop is REQUIRED** - Users must install it separately
- The executable bundles Python and dependencies (~100-200MB)
- First launch may be slower (extracting files)
- Antivirus software may flag the exe (false positive)

### Alternative Approach:
Instead of bundling everything, you could create a simpler launcher that:
1. Checks if Python is installed
2. Checks if dependencies are installed
3. Launches the web UI

This would be smaller but requires users to have Python installed.

## Customization

### Add an Icon:
1. Create or download an `.ico` file
2. Update the `--icon=` parameter:
   ```powershell
   --icon=icon.ico
   ```

### Show Console Window:
Change `--windowed` to `--console` to see debug output

### Include Additional Files:
```powershell
--add-data="path/to/file;destination/path"
```

## Testing

Before distributing:
1. Test on a clean Windows machine (without Python installed)
2. Ensure Docker Desktop is installed
3. Verify the web UI opens correctly
4. Test crawling functionality

## Troubleshooting

### "DLL not found" errors:
- May need to include additional DLLs
- Use `--collect-all` for problematic packages

### Large file size:
- Normal for Python executables (100-200MB+)
- Consider using `--onedir` instead of `--onefile` for faster startup

### Antivirus warnings:
- Common with PyInstaller executables
- Users may need to add exception

