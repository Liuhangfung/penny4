# 🕷️ MediaCrawlerPro - Standalone Edition

**Simple. No Docker. Just Double-Click!**

---

## 📥 Get the Code

### Option 1: Clone from GitHub (Recommended)

```bash
git clone https://github.com/Liuhangfung/penny4.git
cd penny4/MediaCrawlerPro-Python
```

### Option 2: Download ZIP

1. Go to: https://github.com/Liuhangfung/penny4
2. Click **"Code"** → **"Download ZIP"**
3. Extract the ZIP file
4. Navigate to `MediaCrawlerPro-Python` folder

---

## 📋 What You Need

### Prerequisites (One-Time Setup)

1. **Python 3.9 or newer**
   - Download: https://www.python.org/downloads/
   - ⚠️ **IMPORTANT**: During installation, check "**Add Python to PATH**"
   - Verify: Open Command Prompt and type `python --version`

2. **Install Dependencies**
   ```bash
   cd MediaCrawlerPro-Python
   pip install -r requirements.txt
   ```

That's it! **NO Docker required!**

---

## 🚀 Quick Start Guide

### Step 1: Get the Files

Choose one of the options above to get the code from GitHub.

### Step 2: Start the Application

**Double-click `START_MediaCrawler.bat`**

- A terminal window will open
- Browser will automatically open to http://localhost:8501
- Wait 10-15 seconds for the web interface to load

### Step 3: Start Crawling!

1. **Select Platform**: Choose from:
   - Bilibili (bili)
   - Xiaohongshu (xhs)
   - Douyin (dy)
   - Kuaishou (ks)
   - Weibo (wb)
   - Tieba (tieba)
   - Zhihu (zhihu)

2. **Choose Crawler Type**: 
   - `search` - Search by keywords
   - `creator` - Crawl from specific creators

3. **Enter Keywords**: 
   - Example: `deepseek,chatgpt,AI`
   - Separate multiple keywords with commas

4. **Set Max Posts**: How many posts to collect (e.g., 40)

5. **Enable Comments**: Check if you want to collect comments too

6. **Click "Start Crawling"** ▶️

### Step 4: View Results

- Click the **"Data Viewer"** tab to see collected data
- Data refreshes automatically
- Switch between Cards View and Table View
- Download as CSV or JSON

### Step 5: Stop the Application

**Double-click `STOP_MediaCrawler.bat`**

Or simply close the terminal window.

---

## 📁 Folder Structure

```
dist/
├── START_MediaCrawler.bat    ← Double-click to START
├── STOP_MediaCrawler.bat     ← Double-click to STOP
├── web_ui.py                 ← Web interface
├── main.py                   ← Crawler engine
├── config/                   ← Configuration files
│   ├── base_config.py
│   ├── accounts_cookies.xlsx ← Account cookies (optional)
│   └── ...
├── data/                     ← Collected data (auto-created)
│   ├── bilibili/json/
│   ├── xhs/json/
│   └── ...
└── logs/                     ← Log files (auto-created)
    └── bili_search_20251124.log
```

---

## 📊 Where to Find Your Data

### JSON Files

Data is saved to platform-specific folders:

```
data/
├── bilibili/json/search_contents_20251124.json
├── xhs/json/search_contents_20251124.json
├── douyin/json/search_contents_20251124.json
└── ...
```

### CSV Export

1. Go to **Data Viewer** tab
2. Click **"Download as CSV"** button
3. File saves to your Downloads folder

---

## ⚙️ Configuration (Optional)

### Adding Account Cookies

For better results, you can add platform account cookies:

1. Open `config/accounts_cookies.xlsx`
2. Fill in your account cookies
3. Save and restart the app

**How to get cookies:**
- Login to the platform in your browser
- Open Developer Tools (F12)
- Go to Application → Cookies
- Copy the cookie values

### Adjust Crawler Settings

Edit `config/base_config.py`:

```python
# Maximum posts to crawl
CRAWLER_MAX_NOTES_COUNT = 40

# Keywords (comma-separated)
KEYWORDS = "deepseek,chatgpt"

# Enable/disable features
ENABLE_GET_COMMENTS = True
ENABLE_IP_PROXY = False
```

---

## 🐛 Troubleshooting

### Problem: Browser shows "Connection Refused"

**Solution:**
1. Wait 15-20 seconds after starting
2. Make sure the terminal window is still open
3. Try manually going to http://localhost:8501

### Problem: "Python not found"

**Solution:**
1. Install Python from https://www.python.org/downloads/
2. Make sure "Add Python to PATH" was checked
3. Restart your computer
4. Try again

### Problem: "Start Crawling" button is greyed out

**Solution:**
1. Check the sidebar - it should say "Standalone Mode (No Docker)"
2. Make sure you have at least 1 account configured in `config/accounts_cookies.xlsx`
3. Refresh the page

### Problem: Only collecting 1 post

**Solution:**
- Check the log file in `logs/` folder
- Look for error messages
- Common issues:
  - Invalid cookies → Update `accounts_cookies.xlsx`
  - Network issues → Check internet connection
  - Platform rate limiting → Wait a few minutes and try again

### Problem: Port 8501 already in use

**Solution:**
1. Close any other Streamlit applications
2. Run `STOP_MediaCrawler.bat`
3. Open Task Manager → End any "python.exe" processes
4. Try starting again

### Problem: Can't stop the app

**Solution:**
1. Try `STOP_MediaCrawler.bat` first
2. Close the terminal window
3. Open Task Manager (Ctrl+Shift+Esc)
4. Find "python.exe" processes
5. Right-click → End Task

---

## 📝 Log Files

Logs are saved to `logs/` folder:

```
logs/
├── bili_search_20251124_153000.log
├── xhs_search_20251124_154500.log
└── ...
```

To view logs:
1. Go to **Logs** tab in web interface
2. Or open the `.log` file with any text editor

---

## 🎯 Tips for Best Results

### 1. Use Specific Keywords
❌ Bad: "video"
✅ Good: "AI tutorial, deep learning, ChatGPT"

### 2. Start Small
- Test with 10-20 posts first
- Then increase to 100+ once you're familiar

### 3. Add Account Cookies
- Without cookies: Limited data
- With cookies: Full access to posts and comments

### 4. Respect Rate Limits
- Don't crawl too frequently
- Wait a few minutes between large crawls
- Use different keywords to avoid being blocked

### 5. Check Logs
- Always check logs if something goes wrong
- Logs tell you exactly what happened

---

## 🔧 Advanced Usage

### Running from Command Line

```bash
# Navigate to dist folder
cd path/to/dist

# Set environment variables
set USE_DOCKER=false
set ENABLE_SIGN_SERVICE=0

# Run crawler directly
python main.py --platform bili --type search

# Or start web UI
python -m streamlit run web_ui.py --server.port 8501
```

### Batch Processing Multiple Keywords

Edit `config/base_config.py`:

```python
KEYWORDS = "AI,chatgpt,deepseek,claude,gemini,llama"
CRAWLER_MAX_NOTES_COUNT = 100
```

Then run the crawler - it will process all keywords automatically!

---

## 📦 Sharing with Others

To share this with someone else:

1. **Zip the entire `dist` folder**
2. **Include these instructions**
3. **Tell them to install Python first**
4. **That's it!**

What they need:
- ✅ Python 3.9+
- ✅ Your ZIP file
- ❌ NO Docker
- ❌ NO complicated setup

---

## 🌐 Supported Platforms

| Platform | Code | Search | Creator | Comments |
|----------|------|--------|---------|----------|
| Bilibili | bili | ✅ | ✅ | ✅ |
| Xiaohongshu | xhs | ✅ | ✅ | ✅ |
| Douyin | dy | ✅ | ✅ | ✅ |
| Kuaishou | ks | ✅ | ✅ | ✅ |
| Weibo | wb | ✅ | ✅ | ✅ |
| Tieba | tieba | ✅ | ❌ | ✅ |
| Zhihu | zhihu | ✅ | ✅ | ✅ |

---

## 📞 Need Help?

### Check These First:
1. ✅ Python is installed and in PATH
2. ✅ All files are in the same folder
3. ✅ Terminal window is still open
4. ✅ You waited 15+ seconds for startup

### Common Issues:
- **Slow crawling**: Normal! Respects rate limits
- **Only 1 post**: Check account cookies
- **Error messages**: Check log files in `logs/`
- **Can't start**: Close all Python processes and try again

---

## 🎉 You're Ready!

1. **Start**: Double-click `START_MediaCrawler.bat`
2. **Crawl**: Enter keywords and click "Start Crawling"
3. **View**: Check "Data Viewer" tab for results
4. **Export**: Download as CSV or JSON
5. **Stop**: Double-click `STOP_MediaCrawler.bat`

**That's it! Enjoy crawling! 🚀**

---

## ⚖️ Legal Notice

**For educational and research purposes only.**

- ✅ Personal learning and research
- ✅ Small-scale data collection
- ❌ Commercial use
- ❌ Large-scale scraping
- ❌ Violating platform ToS

Please respect platform rules and rate limits.

---

**Last Updated**: November 24, 2024
**Version**: Standalone 1.0

