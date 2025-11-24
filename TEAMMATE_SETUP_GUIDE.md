# 🎯 MediaCrawlerPro - Complete Setup Guide for Teammates

**Goal:** Create a one-click EXE that your friends can use with minimal setup!

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Get the Code](#step-1-get-the-code)
3. [Step 2: Convert BAT to EXE](#step-2-convert-bat-to-exe)
4. [Step 3: Test the EXE](#step-3-test-the-exe)
5. [Step 4: Package for Distribution](#step-4-package-for-distribution)
6. [Step 5: Share with Friends](#step-5-share-with-friends)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### What YOU Need (One-Time Setup):

1. **Git** (to clone the code)
   - Download: https://git-scm.com/download/win
   - Or use GitHub Desktop: https://desktop.github.com/

2. **Docker Desktop** (to test)
   - Download: https://www.docker.com/products/docker-desktop
   - Install and start it

3. **Python 3.9 or newer**
   - Download: https://www.python.org/downloads/
   - ⚠️ **IMPORTANT:** Check "Add Python to PATH" during installation!

---

## Step 1: Get the Code

### Option A: Using Git Command Line

```bash
# Clone the repository
git clone https://github.com/Liuhangfung/penny4.git

# Go to the directory
cd penny4
```

### Option B: Using GitHub Desktop

1. Open GitHub Desktop
2. File → Clone Repository
3. Paste: `https://github.com/Liuhangfung/penny4.git`
4. Click "Clone"

### Option C: Download ZIP

1. Go to: https://github.com/Liuhangfung/penny4
2. Click green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file

---

## Step 2: Convert BAT to EXE

### 🌐 Method 1: Online Converter (FASTEST - 30 seconds!)

1. **Open the converter website:**
   ```
   https://bat2exe.net/
   ```

2. **Upload the BAT file:**
   - Click "Choose File"
   - Navigate to your project folder
   - Select: `MediaCrawlerPro_START.bat`
   - Click "Convert"

3. **Download the EXE:**
   - Wait 5-10 seconds for conversion
   - Click "Download EXE"
   - Save as: `MediaCrawlerPro.exe`
   - Move it to your project folder

4. **Done!** ✅

---

### 🖥️ Method 2: Desktop Software (More Control)

If you prefer desktop software:

1. **Download Bat To Exe Converter:**
   ```
   http://www.f2ko.de/en/b2e.php
   ```

2. **Install and open it**

3. **Convert your BAT file:**
   - Click "Open" button
   - Select: `MediaCrawlerPro_START.bat`
   - (Optional) Add custom icon
   - Click "Compile"
   - Output: `MediaCrawlerPro.exe` will be created

---

## Step 3: Test the EXE

### 🧪 Test on Your Machine First

1. **Make sure Docker Desktop is running**
   - Look for whale icon in system tray
   - Should be active (not paused)

2. **Double-click `MediaCrawlerPro.exe`**

3. **What should happen:**
   ```
   ============================================================
               MediaCrawlerPro Launcher
   ============================================================

   [1/3] Checking Docker Desktop...
   ✅ Docker Desktop is running

   [2/3] Starting services...
   ✅ Services started

   [3/3] Starting Web UI...

   ============================================================
     ✅ MediaCrawlerPro is ready!

     🌐 Opening browser in 3 seconds...
     📍 URL: http://localhost:8501

     ⏹️  Press Ctrl+C to stop
   ============================================================
   ```

4. **Browser opens automatically**
   - Shows MediaCrawlerPro Web UI
   - You can start crawling!

5. **✅ If everything works, proceed to Step 4!**

---

## Step 4: Package for Distribution

### 📦 What to Include in the Package

Create a folder called `MediaCrawlerPro` with these files:

```
MediaCrawlerPro/
├── MediaCrawlerPro.exe          ← The EXE you created
├── docker-compose.yaml          ← Docker configuration
├── web_ui.py                    ← Web interface
├── main.py                      ← Main crawler script
├── config/                      ← Configuration folder
│   ├── base_config.py          ← Settings
│   └── ...                     ← Other config files
├── media_platform/              ← Platform implementations
├── cmd_arg/                     ← Command line args
├── db.py                        ← Database
├── async_db.py                  ← Async database
├── requirements.txt             ← Python dependencies
└── README_FOR_USERS.txt        ← Instructions for friends

(Include all Python files and folders EXCEPT:)
❌ .git/
❌ __pycache__/
❌ dist/
❌ build/
❌ *.pyc
❌ .env (if any)
```

### 📝 Easy Way to Package

1. **Copy the entire project folder**

2. **Delete these folders/files:**
   - `.git/` folder
   - `__pycache__/` folders
   - `dist/` folder
   - `build/` folder
   - Any `.pyc` files

3. **Add your `MediaCrawlerPro.exe`** to the root

4. **Create a ZIP file:**
   - Right-click the folder
   - Send to → Compressed (zipped) folder
   - Name it: `MediaCrawlerPro_v1.0.zip`

---

## Step 5: Share with Friends

### 📤 How to Share

1. **Upload to cloud storage:**
   - Google Drive
   - Dropbox
   - OneDrive
   - WeTransfer

2. **Send the download link to friends**

---

### 📋 Instructions for Your Friends

Send them this message:

---

**Hi! Here's MediaCrawlerPro - a powerful web crawler tool!**

**One-Time Setup (10 minutes):**

1. **Install Docker Desktop** (Required!)
   - Download: https://www.docker.com/products/docker-desktop
   - Install it and start Docker Desktop
   - Wait for the whale icon to appear in system tray

2. **Install Python 3.9+** (Required!)
   - Download: https://www.python.org/downloads/
   - ⚠️ **IMPORTANT:** Check "Add Python to PATH" during installation!

3. **Download & Extract** the MediaCrawlerPro ZIP file I sent you

**How to Use (Every Time):**

1. Make sure Docker Desktop is running (whale icon in system tray)
2. Double-click `MediaCrawlerPro.exe`
3. Browser opens automatically - ready to use! 🎉

**To Stop:**
- Press `Ctrl+C` in the console window
- Or just close the console window

---

## 🔧 Troubleshooting

### Problem: "Docker Desktop is not running"

**Solution:**
- Start Docker Desktop
- Wait for whale icon in system tray
- Run the EXE again

---

### Problem: "Python not found"

**Solution:**
1. Install Python from: https://www.python.org/downloads/
2. ⚠️ Make sure to check "Add Python to PATH"
3. Restart computer
4. Run the EXE again

---

### Problem: "Port 8501 already in use"

**Solution:**
1. Close any other Streamlit apps
2. In PowerShell, run:
   ```powershell
   taskkill /F /IM streamlit.exe
   ```
3. Run the EXE again

---

### Problem: Browser opens but shows "Connection Refused"

**Solution:**
1. Wait 10-15 seconds and refresh the browser
2. Check if Docker containers are running:
   ```bash
   docker ps
   ```
3. If no containers, restart Docker Desktop

---

### Problem: "docker-compose: command not found"

**Solution:**
- Docker Desktop is not installed or not running
- Restart Docker Desktop
- Make sure it's fully started (whale icon not animating)

---

## 📊 What Each File Does

| File | Purpose |
|------|---------|
| `MediaCrawlerPro.exe` | Main launcher - starts everything |
| `docker-compose.yaml` | Configures Docker services (DB, Redis, Sign Service) |
| `web_ui.py` | Streamlit Web UI interface |
| `main.py` | Core crawler script |
| `config/base_config.py` | Settings and configuration |
| `media_platform/` | Platform-specific crawlers (Bilibili, XHS, etc.) |

---

## 🎯 Advanced: Customizing the Crawler

Your friends can edit settings in the Web UI, or manually in:

```
config/base_config.py
```

Key settings:
- `PLATFORM`: "bili", "xhs", "dy", "ks"
- `CRAWLER_TYPE`: "search", "detail", "creator"
- `KEYWORDS`: Search terms
- `CRAWLER_MAX_NOTES_COUNT`: Max items to crawl
- `SAVE_DATA_OPTION`: "json", "csv", "db"

---

## 📧 Support

If you encounter issues:

1. Check the Troubleshooting section above
2. Check Docker Desktop is running
3. Check Python is installed with PATH
4. Check firewall isn't blocking port 8501

---

## 🎉 Success Checklist

- [ ] Cloned/downloaded the code
- [ ] Converted BAT to EXE
- [ ] Tested EXE on your machine
- [ ] Created distribution package (ZIP)
- [ ] Shared with friends
- [ ] Friends successfully set up and running!

---

## 🚀 Next Steps

Once your friends have it working, they can:

1. **Crawl Bilibili, XHS, Douyin, Kuaishou**
2. **Export data to JSON/CSV/MySQL**
3. **Schedule automated crawling**
4. **Analyze data using the exported files**

---

**Questions?** Check the main README.md or reach out!

---

**Created:** 2024
**Version:** 1.0
**Platform:** Windows 10/11

---

**Made with ❤️ using MediaCrawlerPro**

