# 🚀 MediaCrawlerPro Server - Quick Start

Ultra-fast guide to deploy MediaCrawlerPro on your server.

---

## ⚡ Option 1: Automated Setup (Recommended)

**One command to install everything:**

```bash
# 1. Download the setup script
wget https://raw.githubusercontent.com/MediaCrawlerPro/MediaCrawlerPro-Python/main/server_setup.sh

# Or if you have the file locally
# Upload server_setup.sh to your server using SCP/SFTP

# 2. Make it executable
chmod +x server_setup.sh

# 3. Run the setup
bash server_setup.sh
```

**That's it!** The script will:
- ✅ Install Docker & Docker Compose
- ✅ Clone repositories
- ✅ Build images
- ✅ Configure services
- ✅ Start containers

**Time:** ~15-20 minutes

---

## 🔧 Option 2: Manual Setup (Step-by-Step)

### Prerequisites Check
```bash
# You need:
- Ubuntu 20.04+ or Debian 11+
- 4GB RAM minimum
- 20GB disk space
- Root/sudo access
```

### Quick Commands

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 3. Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Create project directory
mkdir -p ~/MediaCrawlerPro && cd ~/MediaCrawlerPro

# 5. Clone Sign Service and build
git clone https://github.com/MediaCrawlerPro/MediaCrawlerPro-SignSrv.git
cd MediaCrawlerPro-SignSrv
docker build -t mediacrawler_signsrv:latest .
cd ..

# 6. Clone Main Project
git clone https://github.com/MediaCrawlerPro/MediaCrawlerPro-Python.git
cd MediaCrawlerPro-Python

# 7. Fix docker-compose (use local image)
sed -i '/image: mediacrawler_signsrv:latest/a\    pull_policy: never' docker-compose.yaml

# 8. Start services
docker-compose up -d

# 9. Verify
docker-compose ps
curl http://localhost:8989/signsrv/pong
```

---

## 📁 Configure Account Cookies

**Upload your `accounts_cookies.xlsx` file:**

```bash
# On your local machine:
scp config/accounts_cookies.xlsx user@server-ip:~/MediaCrawlerPro/MediaCrawlerPro-Python/config/

# Or use SFTP/FileZilla to upload to:
# ~/MediaCrawlerPro/MediaCrawlerPro-Python/config/accounts_cookies.xlsx
```

---

## 🎨 Start Web UI

```bash
cd ~/MediaCrawlerPro/MediaCrawlerPro-Python

# Install Python dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option 1: Run in screen (recommended for server)
screen -S ui
streamlit run web_ui.py --server.port 8501 --server.address 0.0.0.0
# Press Ctrl+A then D to detach

# Option 2: Run in background
nohup streamlit run web_ui.py --server.port 8501 --server.address 0.0.0.0 > ui.log 2>&1 &
```

**Access UI:** `http://YOUR_SERVER_IP:8501`

---

## 🎯 Run Your First Crawl

### Via Web UI:
1. Open `http://YOUR_SERVER_IP:8501`
2. Select platform: `bili`
3. Select type: `search`
4. Enter keywords: `Python programming`
5. Click **▶️ Start Crawling**

### Via Command Line:
```bash
cd ~/MediaCrawlerPro/MediaCrawlerPro-Python

# Bilibili search
docker-compose run --rm app python main.py --platform bili --type search --keywords "Python"

# Bilibili detail
docker-compose run --rm app python main.py --platform bili --type detail

# Bilibili creator
docker-compose run --rm app python main.py --platform bili --type creator
```

---

## 📊 Essential Commands

```bash
# Check status
docker-compose ps

# View logs
docker-compose logs -f
docker-compose logs -f app      # Main app logs
docker-compose logs -f signsrv  # Sign service logs

# Stop everything
docker-compose down

# Restart services
docker-compose restart

# Rebuild after changes
docker-compose down
docker-compose build
docker-compose up -d
```

---

## 🔒 Open Firewall Ports

```bash
# Allow Web UI
sudo ufw allow 8501/tcp

# Enable firewall (if not already)
sudo ufw enable

# Check status
sudo ufw status
```

---

## 🗄️ Access Database

### MySQL:
```bash
# From server
docker exec -it mysql_db mysql -u root -p123456 media_crawler

# View tables
SHOW TABLES;

# Query data
SELECT * FROM bili_video LIMIT 10;
```

### Redis:
```bash
# From server
docker exec -it redis_cache redis-cli -a 123456

# Test
PING
```

---

## 🐛 Troubleshooting

### Sign Service Not Working?
```bash
# Check if running
docker-compose ps

# Check logs
docker-compose logs signsrv

# Test manually
curl http://localhost:8989/signsrv/pong

# Restart
docker-compose restart signsrv
```

### Can't Access Web UI?
```bash
# Check if Streamlit is running
ps aux | grep streamlit

# Check firewall
sudo ufw status

# Check if port is open
sudo netstat -tulpn | grep 8501
```

### Container Won't Start?
```bash
# Check logs
docker-compose logs app

# Check disk space
df -h

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 📖 Full Documentation

- **Detailed Guide:** `SERVER_DEPLOYMENT_GUIDE.md`
- **Project Docs:** https://github.com/MediaCrawlerPro/MediaCrawlerPro-Python

---

## 💡 Pro Tips

1. **Use screen/tmux** for Web UI - keeps it running after disconnect
2. **Change default passwords** in `docker-compose.yaml`
3. **Set up backups** for MySQL data
4. **Monitor disk space** - crawled data can grow quickly
5. **Use database storage** (`SAVE_DATA_OPTION = "db"`) instead of JSON

---

## ✅ Checklist

- [ ] Docker installed
- [ ] Services running (`docker-compose ps`)
- [ ] Sign service tested (`curl localhost:8989/signsrv/pong`)
- [ ] Account cookies configured
- [ ] Firewall configured
- [ ] Web UI accessible
- [ ] First crawl test completed

---

**Need Help?** Check `SERVER_DEPLOYMENT_GUIDE.md` for detailed instructions!

🎉 **Happy Crawling!**

