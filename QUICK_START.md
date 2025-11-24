# ⚡ Quick Start - 3 Steps Only!

## 📥 Get the Code First

```bash
git clone https://github.com/Liuhangfung/penny4.git
cd penny4/MediaCrawlerPro-Python
pip install -r requirements.txt
```

Or download ZIP from: https://github.com/Liuhangfung/penny4

---

## What You Need
- **Python 3.9+** installed (with "Add to PATH" checked)
- **Dependencies installed** (run `pip install -r requirements.txt`)

---

## 🚀 3 Simple Steps

### Step 1: Start
**Double-click** `START_MediaCrawler.bat` (in the `MediaCrawlerPro-Python` folder)
- Wait 15 seconds
- Browser opens automatically

### Step 2: Crawl
1. Select platform (e.g., Bilibili)
2. Type keywords: `deepseek,chatgpt`
3. Set max posts: `40`
4. Click **"Start Crawling"** ▶️

### Step 3: View Data
- Click **"Data Viewer"** tab
- Download as CSV or JSON
- Done! 🎉

---

## 🛑 To Stop
**Double-click** `STOP_MediaCrawler.bat`

---

## 📁 Where's My Data?
```
data/
├── bilibili/json/search_contents_20251124.json
├── xhs/json/search_contents_20251124.json
└── ...
```

---

## 🐛 Problems?

**App won't start?**
- Install Python first: https://www.python.org/downloads/
- Check "Add Python to PATH" during install
- Restart computer

**Only collecting 1 post?**
- Add account cookies to `config/accounts_cookies.xlsx`
- Check log files in `logs/` folder

**Port 8501 in use?**
- Run `STOP_MediaCrawler.bat`
- Close all Python processes
- Try again

---

## 📖 Need More Help?
Read the full **README.md** for detailed instructions!

---

**That's it! You're ready to crawl! 🎯**

