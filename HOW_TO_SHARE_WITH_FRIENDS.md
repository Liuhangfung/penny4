# How to Share MediaCrawlerPro with Your Friends

Easy guide to package and share this with your friends!

---

## 📦 What to Share

Create a ZIP file with these files:

```
MediaCrawlerPro/
├── MediaCrawlerPro_START.bat    ← Main launcher (double-click to run!)
├── README_FOR_USERS.txt         ← Instructions for your friends
├── docker-compose.yaml          ← Docker configuration
├── Dockerfile                   ← Docker image config
├── web_ui.py                    ← Web interface
├── main.py                      ← Main crawler script
├── config/                      ← Configuration folder
│   └── accounts_cookies.xlsx    ← (Optional) Pre-configured cookies
└── [all other Python files]     ← All .py files
```

---

## 🎯 Quick Steps

### Step 1: Create Distribution Folder

```powershell
# Run the package script
python package_for_distribution.py
```

This creates: `MediaCrawlerPro-Distribution/` folder

### Step 2: Add the BAT Launcher

```powershell
# Copy the new launcher
Copy-Item MediaCrawlerPro_START.bat MediaCrawlerPro-Distribution/
Copy-Item README_FOR_USERS.txt MediaCrawlerPro-Distribution/
```

### Step 3: Create ZIP File

```powershell
# Create ZIP for sharing
Compress-Archive -Path "MediaCrawlerPro-Distribution" -DestinationPath "MediaCrawlerPro-v1.0.zip" -Force
```

### Step 4: Share!

Upload `MediaCrawlerPro-v1.0.zip` to:
- Google Drive
- Dropbox
- OneDrive  
- WeTransfer
- Or share directly!

---

## 📋 What Your Friends Need

Tell your friends they need **2 things** installed first:

### 1. Docker Desktop (REQUIRED!)
- **Download**: https://www.docker.com/products/docker-desktop
- **Install**: Takes 5 minutes
- **Start**: Make sure Docker Desktop is running (whale icon in tray)

### 2. Python 3.9+ (REQUIRED!)
- **Download**: https://www.python.org/downloads/
- **Install**: Takes 2 minutes
- ⚠️ **IMPORTANT**: Check "Add Python to PATH" when installing!

---

## 🚀 How Friends Use It

Super simple! Just 3 steps:

1. **Extract ZIP** to any folder
2. **Double-click** `MediaCrawlerPro_START.bat`
3. **Browser opens** automatically → Start crawling!

First time:
- Downloads Docker images (~1-2GB, takes 2-3 minutes)
- Auto-installs Python packages
- After that, starts instantly!

---

## 💬 What to Tell Your Friends

Copy and paste this message:

```
Hey! I'm sharing MediaCrawlerPro with you - it's super easy to use!

📥 Download the ZIP file I sent
📦 Extract it anywhere

Before running, install these (one-time setup):
1. Docker Desktop: https://www.docker.com/products/docker-desktop
2. Python: https://www.python.org/downloads/
   ⚠️ Make sure to check "Add Python to PATH"!

After installing:
1. Start Docker Desktop (wait for whale icon)
2. Double-click MediaCrawlerPro_START.bat
3. Browser opens automatically!

Read README_FOR_USERS.txt for detailed instructions.

Enjoy! 🎉
```

---

## 🎓 Technical Details

### What the BAT File Does:

1. ✅ Checks if Docker Desktop is running
   - If not: Shows message + opens Docker download page
   
2. ✅ Starts Docker services automatically
   - MySQL, Redis, Sign Service
   
3. ✅ Checks if Python is installed
   - If not: Shows message + opens Python download page
   
4. ✅ Auto-installs Python dependencies
   - streamlit, pandas, openpyxl, pymysql, httpx
   - Only on first run!
   
5. ✅ Starts Web UI
   - Opens browser to localhost:8501
   - Ready to crawl!

### Why Not a Single EXE?

- Streamlit has many static files (hard to bundle)
- Python + BAT approach is more reliable
- Still super easy for users (just 2 installs + double-click)
- Much smaller download size
- Easier to update

### System Requirements:

- Windows 10/11 (64-bit)
- 4GB RAM minimum (8GB recommended)
- 5GB free disk space (for Docker images)
- Internet connection

---

## ✅ Testing Before Sharing

Before sharing with friends, test on a clean machine:

1. ✅ Fresh Windows install (or virtual machine)
2. ✅ Install only Docker Desktop + Python
3. ✅ Extract your ZIP file
4. ✅ Double-click MediaCrawlerPro_START.bat
5. ✅ Verify it works!

---

## 🔧 Troubleshooting Guide for Friends

Include this in your message:

**Common Issues:**

❌ "Docker Desktop is not running"
→ Start Docker Desktop, wait for whale icon

❌ "Python not found"
→ Install Python with "Add to PATH" option

❌ Browser doesn't open
→ Manually go to http://localhost:8501

❌ Services won't start
→ Wait 30 seconds and try again

---

## 📊 Features to Highlight

Tell your friends they can:

✅ Crawl from 7 platforms (Bilibili, XHS, Douyin, Kuaishou, Weibo, Tieba, Zhihu)
✅ Search by keywords
✅ Get post details + comments
✅ Crawl creator profiles
✅ Export data as CSV or JSON
✅ Beautiful web interface (no coding needed!)
✅ All data stored in MySQL (easy to query)

---

## 🎉 You're Ready!

Your friends will love how easy this is! Just:
1. Create the ZIP
2. Share it
3. Send them the message above

They'll be crawling in minutes! 🚀

---

**For educational purposes only!**

