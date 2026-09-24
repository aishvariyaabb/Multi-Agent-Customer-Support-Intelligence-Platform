#!/bin/bash
# Setup script for initializing the application on macOS/Linux

echo "🚀 Multi-Agent Customer Support Platform - Setup Script"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $python_version"

# Create .env file if it doesn't exist
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
fi

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p data
mkdir -p logs
mkdir -p notebooks
mkdir -p backend/models
echo "✅ Directories created"

# Create virtual environment and install dependencies
echo ""
echo "🔧 Installing dependencies..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Initialize database
echo ""
echo "🗄️  Initializing database..."
python3 -c "
import sys
sys.path.insert(0, '.')
from backend.database import db_manager
db_manager.create_tables()
print('✅ Database initialized')
"

# Generate sample data
echo ""
echo "📊 Generating sample datasets..."
python3 data/dataset_generator.py

# Print summary
echo ""
echo "=================================================="
echo "✅ Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Configure your .env file:"
echo "   - Edit: .env"
echo "   - Set OPENAI_API_KEY if using OpenAI"
echo "   - Configure DATABASE_URL if needed"
echo ""
echo "2. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Start the backend API:"
echo "   cd backend"
echo "   python main.py"
echo ""
echo "4. Start the frontend (in another terminal):"
echo "   cd frontend"
echo "   streamlit run app.py"
echo ""
echo "5. Access the application:"
echo "   - API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Frontend: http://localhost:8501"
echo ""
echo "=================================================="
