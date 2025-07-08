#!/usr/bin/env python3
"""
Setup Script for Healthcare Startup Discovery System
==================================================

Automated setup and installation script.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print the setup banner."""
    print("=" * 60)
    print("🏥 Healthcare Startup Discovery System - Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_virtual_environment():
    """Create a virtual environment."""
    print("\n📦 Creating virtual environment...")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_pip_command():
    """Get the appropriate pip command for the virtual environment."""
    if platform.system() == "Windows":
        return "venv\\Scripts\\pip"
    else:
        return "venv/bin/pip"

def get_python_command():
    """Get the appropriate python command for the virtual environment."""
    if platform.system() == "Windows":
        return "venv\\Scripts\\python"
    else:
        return "venv/bin/python"

def install_dependencies():
    """Install Python dependencies."""
    print("\n📚 Installing Python dependencies...")
    
    pip_cmd = get_pip_command()
    
    try:
        # Upgrade pip first
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def install_browser_dependencies():
    """Install browser automation dependencies."""
    print("\n🌐 Installing browser dependencies...")
    
    python_cmd = get_python_command()
    
    try:
        # Install Playwright browsers
        subprocess.run([python_cmd, "-m", "playwright", "install"], check=True)
        print("✅ Playwright browsers installed")
        
        # Check for Chrome/Chromium
        chrome_available = False
        
        # Try to find Chrome/Chromium
        chrome_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
        
        for path in chrome_paths:
            if Path(path).exists():
                chrome_available = True
                print(f"✅ Chrome/Chromium found at: {path}")
                break
        
        if not chrome_available:
            print("⚠️  Chrome/Chromium not found. Selenium may not work.")
            print("   Install Chrome or use Playwright instead.")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install browser dependencies: {e}")
        return False

def download_nltk_data():
    """Download required NLTK data."""
    print("\n📖 Downloading NLTK data...")
    
    python_cmd = get_python_command()
    
    try:
        nltk_script = """
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
print("NLTK data downloaded successfully")
"""
        
        subprocess.run([python_cmd, "-c", nltk_script], check=True)
        print("✅ NLTK data downloaded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to download NLTK data: {e}")
        return False

def create_output_directory():
    """Create output directory."""
    print("\n📁 Creating output directory...")
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    print("✅ Output directory created")
    return True

def run_tests():
    """Run the test suite."""
    print("\n🧪 Running tests...")
    
    python_cmd = get_python_command()
    
    try:
        result = subprocess.run([python_cmd, "test_discovery.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("⚠️  Some tests failed. Check the output above.")
            print("You can still use the system, but some features may not work.")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def create_activation_script():
    """Create activation script for easy use."""
    print("\n📝 Creating activation script...")
    
    if platform.system() == "Windows":
        script_content = """@echo off
echo Activating Healthcare Startup Discovery Environment...
call venv\\Scripts\\activate
echo.
echo Environment activated! You can now run:
echo   python healthcare_startup_discovery.py
echo   python test_discovery.py
echo.
"""
        script_path = "activate.bat"
    else:
        script_content = """#!/bin/bash
echo "Activating Healthcare Startup Discovery Environment..."
source venv/bin/activate
echo ""
echo "Environment activated! You can now run:"
echo "  python healthcare_startup_discovery.py"
echo "  python test_discovery.py"
echo ""
"""
        script_path = "activate.sh"
        # Make executable
        os.chmod(script_path, 0o755)
    
    with open(script_path, "w") as f:
        f.write(script_content)
    
    print(f"✅ Activation script created: {script_path}")
    return True

def print_usage_instructions():
    """Print usage instructions."""
    print("\n" + "=" * 60)
    print("🚀 SETUP COMPLETE!")
    print("=" * 60)
    print()
    print("To use the Healthcare Startup Discovery System:")
    print()
    
    if platform.system() == "Windows":
        print("1. Activate the environment:")
        print("   activate.bat")
        print()
        print("2. Run the discovery system:")
        print("   python healthcare_startup_discovery.py")
        print()
        print("3. Run tests:")
        print("   python test_discovery.py")
    else:
        print("1. Activate the environment:")
        print("   source activate.sh")
        print("   # or manually: source venv/bin/activate")
        print()
        print("2. Run the discovery system:")
        print("   python healthcare_startup_discovery.py")
        print()
        print("3. Run tests:")
        print("   python test_discovery.py")
    
    print()
    print("📁 Results will be saved in the 'output' directory")
    print("📝 Logs will be saved in 'output/discovery.log'")
    print()
    print("For more information, see README.md")

def main():
    """Main setup function."""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Install browser dependencies
    if not install_browser_dependencies():
        print("⚠️  Browser dependencies failed, but continuing...")
    
    # Download NLTK data
    if not download_nltk_data():
        sys.exit(1)
    
    # Create output directory
    create_output_directory()
    
    # Create activation script
    create_activation_script()
    
    # Run tests
    run_tests()
    
    # Print usage instructions
    print_usage_instructions()

if __name__ == "__main__":
    main()