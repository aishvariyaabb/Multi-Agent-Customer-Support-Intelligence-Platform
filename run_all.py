"""
Main project initialization and startup script
Run this to start the entire system
"""
import os
import sys
import subprocess
import time
from pathlib import Path
import platform


def print_banner():
    """Print welcome banner"""
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║   🤖 Multi-Agent Customer Support Intelligence Platform       ║
    ║                                                                ║
    ║   Start Script v1.0                                            ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """)


def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        print(f"   Current version: {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def check_dependencies():
    """Check if dependencies are installed"""
    try:
        import fastapi
        import streamlit
        import sqlalchemy
        import pandas
        import sklearn
        print("✅ Core dependencies found")
        return True
    except ImportError as e:
        print(f"⚠️  Missing dependencies: {e}")
        return False


def start_backend():
    """Start FastAPI backend"""
    print("\n🚀 Starting FastAPI Backend...")
    
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    print("   Backend will start at: http://localhost:8000")
    print("   API Docs at: http://localhost:8000/docs")
    
    # Start backend
    if platform.system() == "Windows":
        subprocess.Popen([sys.executable, "main.py"])
    else:
        subprocess.Popen([sys.executable, "main.py"])
    
    print("✅ Backend started (give it 3 seconds to initialize...)")
    time.sleep(3)


def start_frontend():
    """Start Streamlit frontend"""
    print("\n📊 Starting Streamlit Frontend...")
    
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    print("   Frontend will start at: http://localhost:8501")
    
    # Start frontend
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py"])
    
    print("✅ Frontend started")


def main():
    """Main startup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Check dependencies
    if not check_dependencies():
        print("\n⚠️  Installing dependencies...")
        os.system(f"{sys.executable} -m pip install -r requirements.txt")
    
    # Change to project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("\n📋 Project root:", project_root)
    
    # Start components
    print("\n" + "="*60)
    print("Starting all components...")
    print("="*60)
    
    start_backend()
    start_frontend()
    
    # Print final instructions
    print("\n" + "="*60)
    print("✅ All systems started successfully!")
    print("="*60)
    print("""
📝 Access the application:
    • Frontend (Streamlit): http://localhost:8501
    • API Server: http://localhost:8000
    • API Documentation: http://localhost:8000/docs

💡 Tips:
    • Check logs in the logs/ directory
    • Use the QUICK_START.md for detailed guide
    • Read README.md for comprehensive documentation

⚠️  Keep this terminal open. Close it to stop all services.
    """)
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        print("✅ Application stopped")


if __name__ == "__main__":
    main()
