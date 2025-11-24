#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MediaCrawlerPro Launcher
This script checks prerequisites and launches the web UI
"""

import subprocess
import sys
import os
import webbrowser
import time
from pathlib import Path

def check_docker():
    """Check if Docker is installed and running"""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # Check if Docker daemon is running
            result = subprocess.run(
                ["docker", "ps"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        return False
    except Exception:
        return False

def check_docker_compose():
    """Check if docker-compose is available"""
    try:
        result = subprocess.run(
            ["docker-compose", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False

def start_docker_services():
    """Start Docker services if not running"""
    project_dir = Path(__file__).parent.absolute()
    
    try:
        # Check if services are running
        result = subprocess.run(
            ["docker-compose", "ps"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=str(project_dir)
        )
        
        # Start services if needed
        if "Up" not in result.stdout:
            print("🚀 Starting Docker services...")
            subprocess.run(
                ["docker-compose", "up", "-d"],
                cwd=str(project_dir),
                timeout=30
            )
            print("✅ Docker services started!")
            time.sleep(5)  # Wait for services to initialize
    except Exception as e:
        print(f"⚠️  Could not start Docker services: {e}")
        return False
    
    return True

def launch_web_ui():
    """Launch the Streamlit web UI"""
    # Get the directory where the exe is located
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        project_dir = Path(sys.executable).parent
    else:
        # Running as script
        project_dir = Path(__file__).parent.absolute()
    
    web_ui_path = project_dir / "web_ui.py"
    
    if not web_ui_path.exists():
        print(f"❌ Error: web_ui.py not found at {web_ui_path}")
        print(f"   Please ensure web_ui.py is in the same directory as the executable")
        input("Press Enter to exit...")
        return False
    
    print("🌐 Launching Web UI...")
    print("   The web browser will open automatically")
    print("   If not, go to: http://localhost:8501")
    print("\n   Press Ctrl+C to stop the server")
    print()
    
    # Launch Streamlit
    try:
        # Open browser after a delay
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open("http://localhost:8501")
            except Exception:
                pass
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Run Streamlit
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(web_ui_path), "--server.port", "8501", "--server.headless", "true"],
            cwd=str(project_dir)
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        return True
    except Exception as e:
        print(f"❌ Error launching web UI: {e}")
        input("Press Enter to exit...")
        return False

def main():
    """Main launcher function"""
    print("=" * 60)
    print("🕷️  MediaCrawlerPro Launcher")
    print("=" * 60)
    print()
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not installed or not running!")
        print()
        print("📦 Please install Docker Desktop:")
        print("   https://www.docker.com/products/docker-desktop")
        print()
        print("⚠️  Docker Desktop must be running before using MediaCrawlerPro")
        input("Press Enter to exit...")
        return False
    
    print("✅ Docker is installed and running")
    
    # Check docker-compose
    if not check_docker_compose():
        print("⚠️  docker-compose not found, but continuing...")
    else:
        print("✅ docker-compose is available")
    
    # Start Docker services
    print("\n🔧 Checking Docker services...")
    start_docker_services()
    
    # Launch web UI
    print("\n" + "=" * 60)
    launch_web_ui()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

