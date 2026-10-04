"""
Project validation and health check script
"""
import os
import sys
from pathlib import Path


def check_structure():
    """Check project structure"""
    print("🔍 Checking project structure...")
    
    required_dirs = [
        "backend",
        "backend/agents",
        "backend/database",
        "backend/models",
        "backend/rag",
        "backend/config",
        "backend/utils",
        "backend/api",
        "frontend",
        "data",
        "logs",
        "notebooks",
        "tests"
    ]
    
    project_root = Path(__file__).parent
    
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ (missing)")
            return False
    
    return True


def check_files():
    """Check critical files"""
    print("\n📄 Checking critical files...")
    
    required_files = [
        "requirements.txt",
        ".env.example",
        "README.md",
        "QUICK_START.md",
        "setup.py",
        "backend/main.py",
        "backend/__init__.py",
        "backend/agents/__init__.py",
        "backend/database/models.py",
        "backend/config/settings.py",
        "backend/rag/rag_pipeline.py",
        "backend/api/app.py",
        "backend/api/routes.py",
        "frontend/app.py",
        "data/dataset_generator.py"
    ]
    
    project_root = Path(__file__).parent
    missing_files = []
    
    for file_name in required_files:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"  ✅ {file_name}")
        else:
            print(f"  ❌ {file_name} (missing)")
            missing_files.append(file_name)
    
    return len(missing_files) == 0


def check_dependencies():
    """Check installed dependencies"""
    print("\n📦 Checking dependencies...")
    
    dependencies = {
        "fastapi": "FastAPI framework",
        "streamlit": "Streamlit UI",
        "sqlalchemy": "Database ORM",
        "sklearn": "Scikit-learn ML",
        "pandas": "Data processing",
        "numpy": "Numerical computing",
        "faiss": "Vector search (FAISS)",
        "sentence_transformers": "Text embeddings",
        "loguru": "Logging",
    }
    
    missing_deps = []
    
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"  ✅ {module} - {description}")
        except ImportError:
            print(f"  ❌ {module} - {description} (not installed)")
            missing_deps.append(module)
    
    return len(missing_deps) == 0


def check_database():
    """Check database setup"""
    print("\n🗄️  Checking database...")
    
    project_root = Path(__file__).parent
    db_file = project_root / "tickets.db"
    
    if db_file.exists():
        print(f"  ✅ Database exists at {db_file}")
    else:
        print(f"  ⚠️  Database not found at {db_file}")
        print(f"      Run: python setup.py")
    
    return True


def check_env():
    """Check environment configuration"""
    print("\n⚙️  Checking environment configuration...")
    
    project_root = Path(__file__).parent
    env_file = project_root / ".env"
    
    if env_file.exists():
        print(f"  ✅ .env file exists")
    else:
        env_example = project_root / ".env.example"
        if env_example.exists():
            print(f"  ⚠️  .env file not found")
            print(f"      Copy from .env.example: copy .env.example .env")
        else:
            print(f"  ❌ Neither .env nor .env.example found")
    
    return True


def print_summary(results):
    """Print summary"""
    print("\n" + "="*60)
    print("📋 VALIDATION SUMMARY")
    print("="*60)
    
    all_passed = all(results.values())
    
    if all_passed:
        print("✅ All checks passed! Project is ready to run.")
        print("\nNext steps:")
        print("  1. python setup.py         (if first time)")
        print("  2. python run_all.py       (start all services)")
    else:
        print("❌ Some checks failed. Fix issues before running.")
        print("\nFailed checks:")
        for check, passed in results.items():
            if not passed:
                print(f"  • {check}")


def main():
    """Main validation function"""
    print("="*60)
    print("🔍 MULTI-AGENT PLATFORM - PROJECT VALIDATION")
    print("="*60 + "\n")
    
    results = {
        "Project Structure": check_structure(),
        "Critical Files": check_files(),
        "Dependencies": check_dependencies(),
        "Database": check_database(),
        "Environment": check_env(),
    }
    
    print_summary(results)
    
    all_passed = all(results.values())
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
