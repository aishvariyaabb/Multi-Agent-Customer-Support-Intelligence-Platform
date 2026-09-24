"""
Setup script for initializing the application
"""
import os
import sys
import subprocess
from pathlib import Path


def setup_environment():
    """Set up the development environment"""
    
    print("🚀 Multi-Agent Customer Support Platform - Setup Script\n")
    
    project_root = Path(__file__).parent
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        sys.exit(1)
    
    print("✅ Python version check passed")
    
    # Create .env if it doesn't exist
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        print("\n📝 Creating .env file from .env.example...")
        with open(env_example, 'r') as f:
            content = f.read()
        with open(env_file, 'w') as f:
            f.write(content)
        print("✅ .env file created")
    
    # Create necessary directories
    print("\n📁 Creating directories...")
    directories = [
        project_root / "data",
        project_root / "logs",
        project_root / "notebooks",
        project_root / "backend" / "models",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")
    
    # Initialize database
    print("\n🗄️  Initializing database...")
    try:
        os.chdir(project_root)
        
        # Add project root to path
        sys.path.insert(0, str(project_root))
        
        from backend.database import db_manager
        db_manager.create_tables()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")
    
    # Generate sample data
    print("\n📊 Generating sample datasets...")
    try:
        from data.dataset_generator import SampleDatasetGenerator
        SampleDatasetGenerator.generate_all_datasets(str(project_root / "data"))
        print("✅ Sample datasets generated")
    except Exception as e:
        print(f"⚠️  Sample data generation warning: {e}")
    
    # Print summary
    print("\n" + "="*50)
    print("✅ Setup completed successfully!\n")
    print("📋 Next steps:\n")
    print("1. Configure your .env file:")
    print(f"   - Edit: {env_file}")
    print("   - Set OPENAI_API_KEY if using OpenAI")
    print("   - Configure DATABASE_URL if needed\n")
    print("2. Start the backend API:")
    print("   cd backend")
    print("   python main.py\n")
    print("3. Start the frontend (in another terminal):")
    print("   cd frontend")
    print("   streamlit run app.py\n")
    print("4. Access the application:")
    print("   - API: http://localhost:8000")
    print("   - API Docs: http://localhost:8000/docs")
    print("   - Frontend: http://localhost:8501\n")
    print("="*50)


if __name__ == "__main__":
    try:
        setup_environment()
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
