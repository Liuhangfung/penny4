================================================================================
                    MediaCrawlerPro - Installation Guide
================================================================================

Thank you for using MediaCrawlerPro! Follow these simple steps to get started.

================================================================================
                            SYSTEM REQUIREMENTS
================================================================================

1. Operating System: Windows 10 or Windows 11 (64-bit)
2. RAM: Minimum 4GB (8GB recommended)
3. Disk Space: At least 5GB free space
4. Internet Connection: Required

================================================================================
                         STEP 1: INSTALL DOCKER DESKTOP
================================================================================

⚠️  IMPORTANT: Docker Desktop is REQUIRED for MediaCrawlerPro to work!

1. Download Docker Desktop:
   👉 https://www.docker.com/products/docker-desktop

2. Install Docker Desktop:
   - Run the installer
   - Follow the installation wizard
   - Restart your computer if prompted

3. Start Docker Desktop:
   - Find "Docker Desktop" in your Start Menu
   - Launch it and wait for it to start
   - You should see a whale icon in your system tray
   - Make sure Docker Desktop is running (not just installed)

================================================================================
                      STEP 2: RUN MEDIACRAWLERPRO
================================================================================

1. Make sure Docker Desktop is running (check system tray)

2. Double-click: MediaCrawlerPro.exe

3. Wait a few seconds - the program will:
   ✓ Check Docker
   ✓ Start services
   ✓ Open your web browser automatically

4. If the browser doesn't open, manually go to:
   👉 http://localhost:8501

================================================================================
                    STEP 3: CONFIGURE ACCOUNT COOKIES
================================================================================

To crawl data, you need to add your platform account cookies:

1. Install Cookie-Editor browser extension:
   Chrome: https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm
   
2. Login to the platform you want to crawl:
   - Bilibili: https://www.bilibili.com
   - XiaoHongShu (小红书): https://www.xiaohongshu.com
   - Douyin (抖音): https://www.douyin.com
   - Weibo (微博): https://m.weibo.cn
   - Zhihu (知乎): https://www.zhihu.com

3. Export cookies using Cookie-Editor (JSON format)

4. In MediaCrawlerPro Web UI:
   - Go to Settings tab
   - Upload your cookies
   - Or manually edit: config/accounts_cookies.xlsx

================================================================================
                         STEP 4: START CRAWLING!
================================================================================

1. In the Web UI Control Panel:
   
   - Select Platform: bili (Bilibili), xhs (XiaoHongShu), dy (Douyin), etc.
   - Select Type: search, detail, creator, or homefeed
   - Enter Keywords: What you want to search for
   - Set Max Posts: How many posts to collect
   - Enable Comments: Check if you want comments too

2. Click "▶️ Start Crawling"

3. Go to "Data Viewer" tab to see your collected data!

4. Download your data as CSV or JSON

================================================================================
                            TROUBLESHOOTING
================================================================================

❌ "Docker is not installed or not running"
   Solution: Install Docker Desktop and make sure it's running
   Check system tray for Docker whale icon

❌ "Sign Service Not Running"  
   Solution: Wait 30 seconds and refresh the page
   Or restart MediaCrawlerPro.exe

❌ "No Accounts Configured"
   Solution: Add your account cookies (see Step 3)

❌ Port 8501 already in use
   Solution: Close any other Streamlit apps or restart your computer

❌ Antivirus warning
   Solution: Add MediaCrawlerPro.exe to your antivirus exceptions
   (This is a false positive - the EXE is safe!)

❌ Browser doesn't open automatically
   Solution: Manually open http://localhost:8501 in your browser

================================================================================
                            STOPPING THE APP
================================================================================

To stop MediaCrawlerPro:

1. Close the web browser tab
2. Press Ctrl+C in the console window (if visible)
3. Or close the MediaCrawlerPro window

To stop Docker services:
- Open Docker Desktop
- Click "Containers" 
- Stop the MediaCrawlerPro containers

================================================================================
                          SUPPORTED PLATFORMS
================================================================================

✓ Bilibili (哔哩哔哩) - bili
✓ XiaoHongShu (小红书) - xhs  
✓ Douyin (抖音) - dy
✓ Kuaishou (快手) - ks
✓ Weibo (微博) - wb
✓ Baidu Tieba (百度贴吧) - tieba
✓ Zhihu (知乎) - zhihu

================================================================================
                             DATA STORAGE
================================================================================

Your crawled data is stored in:

1. JSON files: data/ folder
2. MySQL database: localhost:3307
   - User: root
   - Password: 123456 (change in docker-compose.yaml)
   - Database: media_crawler

You can view data in the Web UI "Data Viewer" tab!

================================================================================
                         ADVANCED: WEB UI ACCESS
================================================================================

Web UI: http://localhost:8501
Sign Service: http://localhost:8989
MySQL: localhost:3307
Redis: localhost:6378

================================================================================
                            NEED HELP?
================================================================================

GitHub: https://github.com/MediaCrawlerPro/MediaCrawlerPro-Python
Documentation: See SERVER_DEPLOYMENT_GUIDE.md

================================================================================
                          EDUCATIONAL USE ONLY
================================================================================

⚠️  DISCLAIMER:
This tool is for educational and research purposes only.
- Only crawl publicly available data
- Respect platform Terms of Service
- Do not use for commercial purposes
- Control request frequency responsibly
- Do not perform large-scale crawling

By using this software, you agree to use it responsibly and ethically.

================================================================================
                           THANK YOU! 🎉
================================================================================

Enjoy using MediaCrawlerPro!

For educational purposes only.

