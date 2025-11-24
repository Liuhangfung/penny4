# MediaCrawlerPro Setup Guide

## Current Status
✅ Python dependencies installed
✅ Configuration updated to use JSON storage (no MySQL required)
✅ Configuration updated to use local memory cache (no Redis required)

## What's Still Needed

### 1. Sign Service (REQUIRED)
The project requires a separate sign service to generate request signatures for API calls.

**Setup Steps:**
1. Open a new terminal
2. Navigate to parent directory: `cd ..`
3. Clone the sign service: `git clone https://github.com/MediaCrawlerPro/MediaCrawlerPro-SignSrv`
4. Enter the directory: `cd MediaCrawlerPro-SignSrv`
5. Install Node.js dependencies: `npm install`
6. Start the service: `python app.py` (requires Python and Node.js)

The service will run on `http://localhost:8989`

### 2. Account Cookies (REQUIRED)
You need to manually extract cookies from a logged-in browser session.

**Steps to get cookies:**
1. Install Chrome extension: [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
2. Log in to XiaoHongShu (小红书) at https://www.xiaohongshu.com
3. Click the Cookie-Editor extension icon
4. Click "Export" → "JSON" to copy cookies
5. Open `config/accounts_cookies.xlsx`
6. Paste the cookies in the "xhs" sheet (see example format)

**Alternative: Use Excel Template**
- Open `config/accounts_cookies.xlsx`
- Go to the "xhs" (XiaoHongShu) sheet
- Fill in:
  - `id`: Account number (e.g., 1)
  - `name`: Account name
  - `cookies`: Paste your cookies JSON here
  - `remark`: Optional notes

### 3. IP Proxy (OPTIONAL but recommended)
For stable crawling, you may want to use IP proxies. Check `config/proxy_config.py` for configuration.

## Quick Test

Once you have the sign service running and cookies configured, run:

```powershell
# Set UTF-8 encoding
$env:PYTHONIOENCODING="utf-8"

# Run the crawler
python main.py --platform xhs --type search
```

## Available Platforms and Types

### Platforms:
- `xhs` - XiaoHongShu (小红书)
- `dy` - Douyin (抖音)
- `bili` - Bilibili (哔哩哔哩)
- `ks` - Kuaishou (快手)
- `wb` - Weibo (微博)
- `tieba` - Baidu Tieba (百度贴吧)
- `zhihu` - Zhihu (知乎)

### Types:
- `search` - Search by keywords
- `detail` - Get specific post details
- `creator` - Get creator's posts
- `homefeed` - Get homepage recommendations

## Configuration

Edit `config/base_config.py` to customize:
- `KEYWORDS`: Search keywords (default: "deepseek,chatgpt")
- `CRAWLER_MAX_NOTES_COUNT`: Maximum posts to crawl (default: 40)
- `ENABLE_GET_COMMENTS`: Whether to get comments (default: True)

## Data Output

Data will be saved in JSON format in the project directory.

## Troubleshooting

### Error: "账号池中没有可用的账号"
→ You need to add account cookies to `config/accounts_cookies.xlsx`

### Error: Connection refused to localhost:8989
→ The sign service is not running. Start it following step 1 above.

### Error: Unicode encoding issues
→ Run: `$env:PYTHONIOENCODING="utf-8"` before running the script


