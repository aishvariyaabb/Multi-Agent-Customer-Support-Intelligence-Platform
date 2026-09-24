"""
Startup script that handles dependencies and starts the backend
"""
import subprocess
import sys
import time
import os

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    packages = [
        "pydantic-settings>=2.0.0",
        "pydantic>=2.0.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "sqlalchemy>=2.0.0",
        "loguru>=0.7.2",
        "pandas>=2.1.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "sentence-transformers>=2.2.2",
        "faiss-cpu>=1.7.4",
        "nltk>=3.8.1",
        "textblob>=0.17.1",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
    ]
    
    for package in packages:
        try:
            __import__(package.split(">=")[0].replace("-", "_"))
        except ImportError:
            print(f"  Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])
    
    print("✅ Dependencies ready\n")


def start_backend():
    """Start the backend server"""
    print("🚀 Starting FastAPI Backend Server...")
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Run backend
    subprocess.call([sys.executable, "backend/main.py"])


if __name__ == "__main__":
    install_dependencies()
    start_backend()
