#!/bin/bash
#########################################################
# MediaCrawlerPro Server Setup Script
# 
# This script automates the deployment of MediaCrawlerPro
# on a Linux server (Ubuntu/Debian)
#
# Usage: bash server_setup.sh
#########################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo "======================================================"
    echo "$1"
    echo "======================================================"
    echo ""
}

# Check if running as root
check_root() {
    if [ "$EUID" -eq 0 ]; then 
        print_warning "Running as root. This is okay but not required."
    fi
}

# Check OS
check_os() {
    print_info "Checking operating system..."
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
        print_success "Detected: $OS $VER"
    else
        print_error "Cannot detect OS. This script requires Ubuntu/Debian."
        exit 1
    fi
}

# Update system
update_system() {
    print_header "Step 1: Updating System Packages"
    print_info "Running apt update..."
    sudo apt update -y
    print_info "Running apt upgrade..."
    sudo apt upgrade -y
    print_success "System updated!"
}

# Install Docker
install_docker() {
    print_header "Step 2: Installing Docker"
    
    if command -v docker &> /dev/null; then
        print_success "Docker already installed: $(docker --version)"
        return
    fi
    
    print_info "Installing Docker dependencies..."
    sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
    
    print_info "Adding Docker GPG key..."
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    print_info "Adding Docker repository..."
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    print_info "Installing Docker..."
    sudo apt update -y
    sudo apt install -y docker-ce docker-ce-cli containerd.io
    
    print_success "Docker installed: $(docker --version)"
    
    # Add user to docker group
    print_info "Adding user to docker group..."
    sudo usermod -aG docker $USER
    print_warning "You may need to log out and back in for docker group changes to take effect."
}

# Install Docker Compose
install_docker_compose() {
    print_header "Step 3: Installing Docker Compose"
    
    if command -v docker-compose &> /dev/null; then
        print_success "Docker Compose already installed: $(docker-compose --version)"
        return
    fi
    
    print_info "Downloading Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    
    print_info "Making Docker Compose executable..."
    sudo chmod +x /usr/local/bin/docker-compose
    
    print_success "Docker Compose installed: $(docker-compose --version)"
}

# Install Git
install_git() {
    print_header "Step 4: Installing Git"
    
    if command -v git &> /dev/null; then
        print_success "Git already installed: $(git --version)"
        return
    fi
    
    print_info "Installing Git..."
    sudo apt install -y git
    
    print_success "Git installed: $(git --version)"
}

# Install Python and dependencies
install_python() {
    print_header "Step 5: Installing Python and Dependencies"
    
    print_info "Installing Python 3 and pip..."
    sudo apt install -y python3 python3-pip python3-venv
    
    print_success "Python installed: $(python3 --version)"
}

# Clone repositories
clone_repos() {
    print_header "Step 6: Cloning Repositories"
    
    # Create project directory
    PROJECT_DIR="$HOME/MediaCrawlerPro"
    print_info "Creating project directory: $PROJECT_DIR"
    mkdir -p "$PROJECT_DIR"
    cd "$PROJECT_DIR"
    
    # Clone Sign Service
    if [ -d "MediaCrawlerPro-SignSrv" ]; then
        print_warning "MediaCrawlerPro-SignSrv already exists, skipping..."
    else
        print_info "Cloning Sign Service repository..."
        git clone https://github.com/MediaCrawlerPro/MediaCrawlerPro-SignSrv.git
        print_success "Sign Service cloned!"
    fi
    
    # Clone Main Project
    if [ -d "MediaCrawlerPro-Python" ]; then
        print_warning "MediaCrawlerPro-Python already exists, skipping..."
    else
        print_info "Cloning Main Project repository..."
        git clone https://github.com/MediaCrawlerPro/MediaCrawlerPro-Python.git
        print_success "Main Project cloned!"
    fi
}

# Build Docker images
build_images() {
    print_header "Step 7: Building Docker Images"
    
    PROJECT_DIR="$HOME/MediaCrawlerPro"
    
    # Build Sign Service image
    print_info "Building Sign Service Docker image..."
    cd "$PROJECT_DIR/MediaCrawlerPro-SignSrv"
    docker build -t mediacrawler_signsrv:latest .
    print_success "Sign Service image built!"
    
    # Build Main Project image
    print_info "Building Main Project Docker image..."
    cd "$PROJECT_DIR/MediaCrawlerPro-Python"
    docker build -t mediacrawlerpro-python-app:latest .
    print_success "Main Project image built!"
}

# Configure docker-compose
configure_docker_compose() {
    print_header "Step 8: Configuring Docker Compose"
    
    PROJECT_DIR="$HOME/MediaCrawlerPro/MediaCrawlerPro-Python"
    cd "$PROJECT_DIR"
    
    print_info "Updating docker-compose.yaml to use local images..."
    
    # Add pull_policy: never to signsrv service
    if grep -q "pull_policy: never" docker-compose.yaml; then
        print_warning "docker-compose.yaml already configured"
    else
        sed -i '/image: mediacrawler_signsrv:latest/a\    pull_policy: never' docker-compose.yaml
        print_success "docker-compose.yaml updated!"
    fi
}

# Setup Python virtual environment
setup_venv() {
    print_header "Step 9: Setting Up Python Virtual Environment"
    
    PROJECT_DIR="$HOME/MediaCrawlerPro/MediaCrawlerPro-Python"
    cd "$PROJECT_DIR"
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists, skipping..."
    else
        print_info "Creating virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created!"
    fi
    
    print_info "Installing Python dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Python dependencies installed!"
}

# Configure firewall
configure_firewall() {
    print_header "Step 10: Configuring Firewall (Optional)"
    
    if ! command -v ufw &> /dev/null; then
        print_warning "UFW not installed, skipping firewall configuration..."
        return
    fi
    
    read -p "Do you want to configure UFW firewall? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Enabling UFW..."
        sudo ufw --force enable
        
        print_info "Allowing SSH (port 22)..."
        sudo ufw allow 22/tcp
        
        print_info "Allowing Web UI (port 8501)..."
        sudo ufw allow 8501/tcp
        
        print_info "Firewall rules:"
        sudo ufw status
        
        print_success "Firewall configured!"
    else
        print_info "Skipping firewall configuration"
    fi
}

# Start Docker services
start_services() {
    print_header "Step 11: Starting Docker Services"
    
    PROJECT_DIR="$HOME/MediaCrawlerPro/MediaCrawlerPro-Python"
    cd "$PROJECT_DIR"
    
    print_info "Starting Docker containers..."
    docker-compose up -d
    
    sleep 5
    
    print_info "Checking container status..."
    docker-compose ps
    
    print_success "Docker services started!"
}

# Test services
test_services() {
    print_header "Step 12: Testing Services"
    
    print_info "Testing Sign Service..."
    sleep 3  # Give services time to fully start
    
    RESPONSE=$(curl -s http://localhost:8989/signsrv/pong)
    
    if [[ $RESPONSE == *"pong"* ]]; then
        print_success "Sign Service is working! Response: $RESPONSE"
    else
        print_error "Sign Service test failed!"
        print_warning "You may need to check the logs: docker-compose logs signsrv"
    fi
}

# Print completion message
print_completion() {
    print_header "🎉 Installation Complete!"
    
    echo ""
    echo "MediaCrawlerPro has been successfully deployed!"
    echo ""
    echo "Next Steps:"
    echo ""
    echo "1. Configure account cookies:"
    echo "   cd ~/MediaCrawlerPro/MediaCrawlerPro-Python/config"
    echo "   # Upload your accounts_cookies.xlsx file here"
    echo ""
    echo "2. Start the Web UI:"
    echo "   cd ~/MediaCrawlerPro/MediaCrawlerPro-Python"
    echo "   source venv/bin/activate"
    echo "   streamlit run web_ui.py --server.port 8501 --server.address 0.0.0.0"
    echo ""
    echo "3. Access the Web UI:"
    echo "   http://$(hostname -I | awk '{print $1}'):8501"
    echo ""
    echo "4. Run a crawl task:"
    echo "   docker-compose run --rm app python main.py --platform bili --type search"
    echo ""
    echo "📚 For more details, see: SERVER_DEPLOYMENT_GUIDE.md"
    echo ""
    echo "Useful commands:"
    echo "  - View logs: docker-compose logs -f"
    echo "  - Stop services: docker-compose down"
    echo "  - Restart services: docker-compose restart"
    echo ""
}

# Main execution
main() {
    print_header "MediaCrawlerPro Server Setup"
    print_info "This script will install and configure MediaCrawlerPro on your server"
    
    read -p "Do you want to continue? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Setup cancelled"
        exit 0
    fi
    
    check_root
    check_os
    update_system
    install_docker
    install_docker_compose
    install_git
    install_python
    clone_repos
    build_images
    configure_docker_compose
    setup_venv
    configure_firewall
    start_services
    test_services
    print_completion
}

# Run main function
main

