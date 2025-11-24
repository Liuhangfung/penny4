# Build Standalone EXE for MediaCrawlerPro

This guide will help you create a **standalone Windows executable** that users can double-click to run MediaCrawlerPro on their own computer using Docker.

---

## 🎯 What This EXE Does

When users double-click `MediaCrawlerPro.exe`:

1. ✅ Checks if Docker Desktop is installed and running on **their computer**
2. ✅ Starts Docker containers **locally** (MySQL, Redis, Sign Service)
3. ✅ Launches Web UI at **http://localhost:8501**
4. ✅ Opens browser automatically
5. ✅ User can start crawling immediately!

**Everything runs on the user's own Windows PC - no server needed!** 🖥️

---

## 📋 Prerequisites (For Building)

You need these **only for building** the EXE (not for end users):

- Windows 10/11
- Python 3.9 or 3.11+
- All project dependencies installed
- PyInstaller

---

## 🚀 Step 1: Install PyInstaller

```powershell
# In your project directory
cd "C:\Users\USER\Desktop\trading analysis\AI Project\Penny\MediaCrawlerPro-Python"

# Install PyInstaller
pip install pyinstaller
```

---

## 🔨 Step 2: Build the EXE

### **Option A: Using the Optimized Build Script (Recommended)**

```powershell
# This creates a smaller, optimized EXE
python build_exe_optimized.py
```

⏳ **Wait 5-10 minutes** while PyInstaller packages everything...

### **Option B: Using the Standard Build Script**

```powershell
# This includes more dependencies (larger file)
python build_exe.py
```

### **Option C: Manual PyInstaller Command**

```powershell
pyinstaller launcher.py `
  --name=MediaCrawlerPro `
  --onefile `
  --windowed `
  --hidden-import=streamlit `
  --hidden-import=pandas `
  --hidden-import=openpyxl `
  --hidden-import=pymysql `
  --hidden-import=httpx `
  --collect-all=streamlit
```

---

## 📦 Step 3: Create Distribution Package

After building the EXE, create a complete package for users:

```powershell
# This creates a folder with everything users need
python package_for_distribution.py
```

This creates: `MediaCrawlerPro-Distribution/` folder with:
- ✅ MediaCrawlerPro.exe
- ✅ docker-compose.yaml
- ✅ Dockerfile
- ✅ config/ folder
- ✅ All necessary Python modules
- ✅ USER_README.txt
- ✅ QUICK_START.txt

---

## 🧪 Step 4: Test the EXE

### **Test on Your Computer First**

```powershell
cd dist
.\MediaCrawlerPro.exe
```

It should:
1. ✅ Check Docker Desktop
2. ✅ Start containers locally
3. ✅ Open browser to http://localhost:8501

### **Test on a Clean Machine (Important!)**

For best results, test on a computer that does NOT have:
- Python installed
- Project dependencies

This ensures the EXE works standalone!

---

## 📤 Step 5: Distribute to Users

### **Option A: Distribute the Full Package**

1. Zip the `MediaCrawlerPro-Distribution` folder
2. Upload to Google Drive, Dropbox, or GitHub Releases
3. Share the download link

### **Option B: Distribute Just the EXE (Simpler)**

If users already have Docker installed:
1. Just share `MediaCrawlerPro.exe`
2. Include `USER_README.txt` for instructions

---

## 📝 User Requirements

Users will need:

1. **Windows 10 or 11** (64-bit)
2. **Docker Desktop** (MUST BE INSTALLED!)
   - Download: https://www.docker.com/products/docker-desktop
   - Docker Desktop MUST be running before launching the EXE
3. **4GB RAM** minimum (8GB recommended)
4. **5GB free disk space**

Users do **NOT** need:
- ❌ Python installation
- ❌ Manual dependency installation
- ❌ Server setup
- ❌ Technical knowledge

---

## 🎓 How Users Use It

### **Step 1: Install Docker Desktop**

Users must download and install Docker Desktop:
https://www.docker.com/products/docker-desktop

### **Step 2: Start Docker Desktop**

Look for the Docker whale icon in the system tray (taskbar).

### **Step 3: Double-Click MediaCrawlerPro.exe**

The EXE will:
1. Check Docker is running
2. Start containers (first time: downloads images ~1-2GB)
3. Launch Web UI
4. Open browser

### **Step 4: Configure Account Cookies**

In the Web UI, users need to add their platform cookies:
1. Install Cookie-Editor extension
2. Login to platform (Bilibili, XHS, etc.)
3. Export cookies
4. Add to MediaCrawlerPro

### **Step 5: Start Crawling!**

Select platform, type, keywords, and click Start!

---

## 📊 File Sizes

- **MediaCrawlerPro.exe**: ~100-200 MB (bundled Python + dependencies)
- **Full Distribution Package**: ~150-250 MB
- **Docker Images** (downloaded on first run): ~1-2 GB

This is normal for Python executables!

---

## 🔧 Troubleshooting

### Build Errors

#### "PyInstaller not found"
```powershell
pip install pyinstaller
```

#### "Module not found" during build
```powershell
pip install -r requirements.txt
```

#### Build takes too long
- Normal! Can take 5-15 minutes
- Be patient, especially on first build

#### "Permission denied" or "Access denied"
- Run PowerShell as Administrator
- Or add exception in antivirus

### Runtime Errors (For Users)

#### "Docker is not installed or not running"
- User needs to install Docker Desktop
- Make sure Docker Desktop is running (whale icon in tray)

#### "Port 8501 already in use"
- Close other Streamlit apps
- Restart computer

#### Antivirus Warnings
- Windows Defender may flag the EXE (false positive)
- Add to exceptions if needed
- This is common with PyInstaller executables

---

## 🎨 Customization

### Add an Icon

1. Create or download a `.ico` file (256x256 recommended)
2. Update build script:

```python
# In build_exe_optimized.py
'--icon=icon.ico',  # Add this line
```

### Change Window Title

Edit `launcher.py`:

```python
print("🕷️  Your Custom Name Here")
```

### Add More Platforms

Already included! Supports:
- Bilibili
- XiaoHongShu
- Douyin
- Kuaishou
- Weibo
- Baidu Tieba
- Zhihu

---

## 🔒 Security Notes

### For Developers

- The EXE bundles your Python environment
- Config files are included but users can modify them
- Consider encrypting sensitive data if needed

### For Users

- Only download from official sources
- Antivirus warnings are false positives (PyInstaller common issue)
- The EXE is safe - it's just bundled Python code

---

## 📈 Advanced: Reducing EXE Size

### Exclude Unused Modules

Edit `build_exe_optimized.py` and add more exclusions:

```python
excludes = [
    'torch',
    'tensorflow',
    'matplotlib',
    'scipy',
    'jupyter',
    # Add more here
]
```

### Use --onedir Instead of --onefile

Faster startup but creates a folder instead of single EXE:

```python
'--onedir',  # Instead of '--onefile'
```

---

## ✅ Distribution Checklist

Before distributing to users:

- [ ] Build EXE successfully
- [ ] Test on your computer (Docker running)
- [ ] Test on clean Windows machine
- [ ] Verify browser opens automatically
- [ ] Test crawling functionality
- [ ] Create distribution package
- [ ] Write clear user instructions
- [ ] Test on Windows 10 and 11
- [ ] Check antivirus doesn't block
- [ ] Create ZIP for distribution

---

## 📞 Support

If users have issues:

1. Check Docker Desktop is running
2. Check Windows Firewall settings
3. Try running as Administrator
4. Check logs in the console window
5. Refer to USER_README.txt

---

## 🎉 Summary

**What you created:**
- ✅ Standalone Windows EXE (no Python needed for users!)
- ✅ Runs everything locally on user's computer
- ✅ Uses Docker for services (MySQL, Redis, Sign Service)
- ✅ Beautiful Web UI
- ✅ One-click to start crawling

**What users need:**
- ✅ Windows 10/11
- ✅ Docker Desktop installed and running
- ✅ Double-click MediaCrawlerPro.exe
- ✅ That's it!

---

**Happy Building! 🚀**

For educational purposes only.

