# MediaCrawlerPro Server Deployment Guide

Complete step-by-step guide to deploy MediaCrawlerPro on a remote server.

---

## 📋 Prerequisites

### What You Need:
- ✅ A Linux server (Ubuntu 20.04+ or Debian 11+ recommended)
- ✅ SSH access to your server
- ✅ Root or sudo privileges
- ✅ At least 4GB RAM, 20GB disk space
- ✅ Open ports: 8501 (Web UI), 8989 (Sign Service), 3307 (MySQL), 6378 (Redis)

---

## 🚀 Step-by-Step Deployment

### Step 1: Connect to Your Server

```bash
# From your local machine
ssh username@your-server-ip

# Example:
# ssh root@192.168.1.100
# or
# ssh user@myserver.com
```

---

### Step 2: Update System Packages

```bash
# Update package lists
sudo apt update

# Upgrade installed packages
sudo apt upgrade -y
```

---

### Step 3: Install Docker

```bash
# Install required packages
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package list again
sudo apt update

# Install Docker
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Verify Docker installation
docker --version
```

**Expected output:** `Docker version 27.x.x, build xxxxx`

---

### Step 4: Install Docker Compose

```bash
# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make it executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

**Expected output:** `Docker Compose version v2.x.x`

---

### Step 5: Configure Docker Permissions (Optional but Recommended)

```bash
# Add your user to docker group (to run docker without sudo)
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Test docker without sudo
docker ps
```

---

### Step 6: Install Git

```bash
# Install git
sudo apt install -y git

# Verify installation
git --version
```

---

### Step 7: Create Project Directory

```bash
# Create a directory for the project
mkdir -p ~/MediaCrawlerPro
cd ~/MediaCrawlerPro
```

---

### Step 8: Clone Sign Service Repository

```bash
# Clone the sign service repository
git clone https://github.com/MediaCrawlerPro/MediaCrawlerPro-SignSrv.git

# Enter the directory
cd MediaCrawlerPro-SignSrv

# Build Docker image for sign service
docker build -t mediacrawler_signsrv:latest .

# Go back to parent directory
cd ..
```

**This will take 3-5 minutes...**

---

### Step 9: Clone Main Project Repository

```bash
# Clone the main project
git clone https://github.com/MediaCrawlerPro/MediaCrawlerPro-Python.git

# Enter the project directory
cd MediaCrawlerPro-Python
```

---

### Step 10: Configure Account Cookies

**IMPORTANT:** You need to add account cookies for the platforms you want to crawl.

```bash
# The cookies file is located at:
# config/accounts_cookies.xlsx

# You have 3 options to upload this file:

# Option 1: Use SCP from your local machine
# (Run this on your LOCAL machine, not the server)
# scp config/accounts_cookies.xlsx username@server-ip:~/MediaCrawlerPro/MediaCrawlerPro-Python/config/

# Option 2: Use SFTP client (FileZilla, WinSCP, etc.)
# Connect to your server and navigate to:
# ~/MediaCrawlerPro/MediaCrawlerPro-Python/config/
# Upload your accounts_cookies.xlsx file

# Option 3: Download the template and edit on server
# Download from browser, get cookies using Cookie-Editor extension
# Then upload the file to the server
```

**How to Get Cookies:**
1. Install [Cookie-Editor Chrome Extension](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
2. Login to your target platform:
   - **Bilibili**: https://www.bilibili.com
   - **XiaoHongShu**: https://www.xiaohongshu.com
   - **Douyin**: https://www.douyin.com
   - **Weibo**: https://m.weibo.cn
3. Export cookies as JSON using Cookie-Editor
4. Add cookies to `config/accounts_cookies.xlsx` in the corresponding sheet

---

### Step 11: Configure Docker Compose (Fix for Local Image)

```bash
# Edit docker-compose.yaml
nano docker-compose.yaml

# Add this line under signsrv service (after "image: mediacrawler_signsrv:latest"):
#   pull_policy: never

# Or use this command to do it automatically:
sed -i '/image: mediacrawler_signsrv:latest/a\    pull_policy: never' docker-compose.yaml
```

The signsrv section should look like:
```yaml
  signsrv:
    image: mediacrawler_signsrv:latest
    pull_policy: never
    container_name: mediacrawler_signsrv
    ...
```

---

### Step 12: Configure Firewall (If Applicable)

```bash
# If you're using UFW firewall
sudo ufw allow 8501/tcp  # Web UI
sudo ufw allow 8989/tcp  # Sign Service (optional - only if accessing externally)
sudo ufw allow 3307/tcp  # MySQL (optional - only if accessing externally)
sudo ufw allow 6378/tcp  # Redis (optional - only if accessing externally)

# Check firewall status
sudo ufw status
```

**Note:** For security, you might want to only allow 8501 (Web UI) and keep others internal to Docker network.

---

### Step 13: Start All Docker Services

```bash
# Make sure you're in the MediaCrawlerPro-Python directory
cd ~/MediaCrawlerPro/MediaCrawlerPro-Python

# Start all services
docker-compose up -d

# Check if all containers are running
docker-compose ps
```

**Expected output:**
```
NAME                   STATUS          PORTS
mediacrawler_signsrv   Up             0.0.0.0:8989->8989/tcp
mysql_db               Up             0.0.0.0:3307->3306/tcp
redis_cache            Up             0.0.0.0:6378->6379/tcp
mediacrawlerpro        Up             0.0.0.0:8000->8000/tcp
```

---

### Step 14: Verify Sign Service is Working

```bash
# Test the sign service
curl http://localhost:8989/signsrv/pong

# Expected response:
# {"biz_code":0,"msg":"OK!","isok":true,"data":{"message":"pong"}}
```

---

### Step 15: Install Python and Streamlit (For Web UI)

```bash
# Install Python 3.9+ and pip
sudo apt install -y python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

**This will take 5-10 minutes...**

---

### Step 16: Start Web UI

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Start Streamlit in background using screen or tmux
# Option 1: Using screen
sudo apt install -y screen
screen -S mediacrawler-ui
streamlit run web_ui.py --server.port 8501 --server.address 0.0.0.0

# Press Ctrl+A, then D to detach from screen
# To reattach: screen -r mediacrawler-ui

# Option 2: Using tmux
sudo apt install -y tmux
tmux new -s mediacrawler-ui
streamlit run web_ui.py --server.port 8501 --server.address 0.0.0.0

# Press Ctrl+B, then D to detach from tmux
# To reattach: tmux attach -t mediacrawler-ui

# Option 3: Run in background with nohup
nohup streamlit run web_ui.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
```

---

### Step 17: Access Web UI

**From Your Browser:**

```
http://YOUR_SERVER_IP:8501

# Example:
# http://192.168.1.100:8501
# or
# http://myserver.com:8501
```

---

## 🎯 Using the Crawler

### Method 1: Via Web UI (Recommended)

1. Open browser: `http://YOUR_SERVER_IP:8501`
2. Select platform (e.g., `bili`)
3. Select crawler type (e.g., `search`)
4. Enter keywords
5. Click "▶️ Start Crawling"

### Method 2: Via Command Line

```bash
# Run a crawl task using docker-compose
docker-compose run --rm app python main.py --platform bili --type search --keywords "Python编程"

# For Bilibili detail crawl
docker-compose run --rm app python main.py --platform bili --type detail

# For Bilibili creator crawl
docker-compose run --rm app python main.py --platform bili --type creator
```

---

## 📊 Monitoring and Logs

### View Container Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f app
docker-compose logs -f signsrv
docker-compose logs -f db
docker-compose logs -f redis

# View Web UI logs (if using nohup)
tail -f streamlit.log
```

### Check Container Status

```bash
# List running containers
docker-compose ps

# Check resource usage
docker stats
```

---

## 🗄️ Database Access

### Connect to MySQL

```bash
# From server
docker exec -it mysql_db mysql -u root -p123456 media_crawler

# From external tool (if port 3307 is open)
# Host: YOUR_SERVER_IP
# Port: 3307
# User: root
# Password: 123456
# Database: media_crawler
```

### Connect to Redis

```bash
# From server
docker exec -it redis_cache redis-cli -a 123456

# Test connection
PING
# Expected: PONG
```

---

## 🔒 Security Best Practices

### 1. Change Default Passwords

```bash
# Edit docker-compose.yaml
nano docker-compose.yaml

# Change these values:
# - MYSQL_ROOT_PASSWORD: 123456  → Change to strong password
# - REDIS_PASSWORD: 123456  → Change to strong password
# - RELATION_DB_PWD: 123456  → Change to match MySQL password
# - REDIS_DB_PWD: 123456  → Change to match Redis password
```

### 2. Use Firewall to Restrict Access

```bash
# Only allow Web UI from specific IPs
sudo ufw allow from YOUR_IP to any port 8501

# Block all other access to database ports
sudo ufw deny 3307/tcp
sudo ufw deny 6378/tcp
```

### 3. Use HTTPS with Nginx Reverse Proxy (Optional)

```bash
# Install Nginx
sudo apt install -y nginx certbot python3-certbot-nginx

# Configure reverse proxy
sudo nano /etc/nginx/sites-available/mediacrawler

# Add this configuration:
```

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/mediacrawler /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com
```

---

## 🔄 Maintenance Commands

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes database data)
docker-compose down -v
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart app
docker-compose restart signsrv
```

### Update Project

```bash
# Stop services
docker-compose down

# Pull latest changes
cd ~/MediaCrawlerPro/MediaCrawlerPro-Python
git pull origin main

# Rebuild images
docker-compose build

# Start services
docker-compose up -d
```

### Clean Up Docker

```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Remove everything unused
docker system prune -a
```

---

## 🐛 Troubleshooting

### Problem: Container won't start

```bash
# Check logs
docker-compose logs app

# Check if ports are already in use
sudo netstat -tulpn | grep 8501
sudo netstat -tulpn | grep 8989
```

### Problem: Sign service connection failed

```bash
# Test sign service
curl http://localhost:8989/signsrv/pong

# Check if container is running
docker-compose ps

# Restart sign service
docker-compose restart signsrv
```

### Problem: Database connection error

```bash
# Check if MySQL is running
docker-compose ps

# Check MySQL logs
docker-compose logs db

# Restart MySQL
docker-compose restart db
```

### Problem: Out of disk space

```bash
# Check disk usage
df -h

# Clean up Docker
docker system prune -a -f

# Clean up logs
truncate -s 0 streamlit.log
```

---

## 📝 Quick Reference

### Useful Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Run a crawl task
docker-compose run --rm app python main.py --platform bili --type search

# Start Web UI (in screen)
screen -S ui
streamlit run web_ui.py --server.port 8501 --server.address 0.0.0.0
# Ctrl+A, D to detach

# Reattach to screen
screen -r ui

# Check container status
docker-compose ps

# Restart service
docker-compose restart app
```

---

## 🎓 Next Steps

1. ✅ Configure your account cookies
2. ✅ Test with a small crawl task
3. ✅ Monitor logs for errors
4. ✅ Set up backups for your data
5. ✅ Configure automated tasks with cron (optional)

---

## 📚 Additional Resources

- **Main Project**: https://github.com/MediaCrawlerPro/MediaCrawlerPro-Python
- **Sign Service**: https://github.com/MediaCrawlerPro/MediaCrawlerPro-SignSrv
- **Docker Documentation**: https://docs.docker.com/
- **Streamlit Documentation**: https://docs.streamlit.io/

---

## 🆘 Need Help?

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify all services are running: `docker-compose ps`
3. Test sign service: `curl http://localhost:8989/signsrv/pong`
4. Check firewall settings
5. Verify account cookies are configured correctly

---

**Good luck with your deployment! 🚀**

