# Multi-Agent Customer Support Intelligence Platform
<img width="1887" height="880" alt="image" src="https://github.com/user-attachments/assets/60ab6349-6c7b-4f72-9482-4c8ae6c41ac9" />
<img width="1833" height="856" alt="image" src="https://github.com/user-attachments/assets/1ae2409d-1c0d-4745-a439-ac45597a69a3" />
<img width="1571" height="857" alt="image" src="https://github.com/user-attachments/assets/f860a7f4-c368-43ff-8b04-9af823ea7d0b" />
<img width="1815" height="852" alt="image" src="https://github.com/user-attachments/assets/fd913dcf-65cd-489a-9e7e-158a525f2f88" />


## 🎯 Overview

A sophisticated AI-powered multi-agent system for automating customer support ticket handling. This platform uses intelligent agents to understand, classify, respond to, and route customer support tickets while continuously learning from outcomes.

## 🌟 Features

✨ **Multi-Agent Architecture**
- Intake Agent: Text preprocessing & entity extraction
- Classification Agent: Category & priority assignment
- Retrieval Agent: RAG-based knowledge base search
- Response Agent: Intelligent response generation
- Escalation Agent: Smart ticket routing
- Learning Agent: Continuous system improvement

🚀 **Key Capabilities**
- Automatic ticket classification (delivery, refund, payment, etc.)
- Sentiment analysis and priority assessment
- Knowledge base integration with FAISS vector search
- Intelligent escalation for complex issues
- Real-time analytics dashboard
- Customer satisfaction tracking
- Feedback-driven learning loop

📊 **Performance Metrics**
- **Target Automation Rate**: 60-70% of tickets auto-resolved
- **Response Time**: <2 seconds per ticket
- **Classification Accuracy**: >85%
- **Customer Satisfaction**: Track and improve over time

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│         Streamlit Frontend (Chat Interface)          │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│              FastAPI Backend                         │
│  (/api/v1/process, /api/v1/tickets, etc.)          │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│        Agent Orchestrator (Workflow Engine)          │
│  ┌────────────────────────────────────────┐         │
│  │  1. IntakeAgent → 2. ClassificationAgent        │
│  │  3. RetrievalAgent → 4. ResponseAgent           │
│  │  5. EscalationAgent → 6. LearningAgent         │
│  └────────────────────────────────────────┘         │
└──────────────────┬──────────────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼──┐      ┌───▼──┐      ┌───▼──────┐
│ FAISS│      │  ML  │      │Database  │
│ RAG  │      │Models│      │ (SQLite/ │
│      │      │      │      │PostgreSQL│
└──────┘      └──────┘      └──────────┘
```

## 🛠️ Technology Stack

### Core
- **Python 3.10+**
- **FastAPI**: REST API backend
- **Streamlit**: Interactive frontend
- **SQLAlchemy**: Database ORM

### AI/ML
- **Scikit-learn**: Classification models
- **HuggingFace Transformers**: NLP models
- **Sentence-Transformers**: Text embeddings
- **LangChain/CrewAI**: Agent orchestration

### Data & Search
- **FAISS**: Vector similarity search
- **SQLite/PostgreSQL**: Relational database
- **MongoDB**: Optional document storage

### Utilities
- **Pandas/NumPy**: Data processing
- **Loguru**: Structured logging
- **Pydantic**: Data validation

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip or conda
- Virtual environment (recommended)

### Setup Steps

1. **Clone and navigate to project**
```bash
cd "e:\GUVI_projects\Multi-Agent Customer Support Intelligence Platform"
```

2. **Create virtual environment**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy example env file
copy .env.example .env

# Edit .env with your settings
# - Set OPENAI_API_KEY if using OpenAI
# - Set DATABASE_URL
# - Configure other settings as needed
```

5. **Initialize database**
```bash
python -c "from backend.database import db_manager; db_manager.create_tables()"
```

6. **Generate sample datasets**
```bash
python data/dataset_generator.py
```

## 🚀 Running the Application

### Start Backend API
```bash
cd backend
python main.py
```
API will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### Start Frontend (in another terminal)
```bash
cd frontend
streamlit run app.py
```
Frontend will be available at `http://localhost:8501`

### Full Setup Script
```bash
# Windows
python scripts/setup.py

# macOS/Linux
bash scripts/setup.sh
```

## 💡 Usage

### 1. Via Streamlit UI
- Navigate to `http://localhost:8501`
- Enter ticket details in the form
- View real-time processing and agent logs
- Track ticket history and analytics

### 2. Via API Endpoints

**Process a ticket:**
```bash
curl -X POST "http://localhost:8000/api/v1/process" \
  -H "Content-Type: application/json" \
  -d {
    "ticket_text": "My order hasn't arrived",
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "enable_rag": true,
    "enable_escalation": true
  }
```

**Get analytics:**
```bash
curl "http://localhost:8000/api/v1/analytics/overview?days=7"
```

**Submit feedback:**
```bash
curl -X POST "http://localhost:8000/api/v1/tickets/{ticket_id}/feedback" \
  -H "Content-Type: application/json" \
  -d {
    "rating": 5,
    "feedback_text": "Great support!",
    "was_helpful": true
  }
```

## 📊 API Endpoints

### Tickets
- `POST /api/v1/tickets` - Create ticket
- `POST /api/v1/process` - Process ticket through pipeline
- `GET /api/v1/tickets/{id}` - Get ticket details
- `POST /api/v1/tickets/{id}/feedback` - Submit feedback

### Analytics
- `GET /api/v1/analytics/overview` - System overview
- `GET /api/v1/analytics/tickets/by-category` - Tickets by category
- `GET /api/v1/analytics/tickets/by-priority` - Tickets by priority

### Knowledge Base
- `POST /api/v1/knowledge-base` - Add KB article
- `GET /api/v1/knowledge-base` - Search KB
- `PUT /api/v1/knowledge-base/{id}` - Update KB article

## 🧪 Testing

Run tests:
```bash
pytest tests/ -v
pytest tests/ --cov=backend
```

Test specific module:
```bash
pytest tests/test_agents.py -v
pytest tests/test_rag.py -v
```

## 📈 Performance Monitoring

### View Logs
```bash
# Recent logs
tail -f logs/app_*.log

# Filter by agent
grep "ClassificationAgent" logs/app_*.log
```

### Metrics Dashboard
- Access `http://localhost:8501` for real-time metrics
- View agent execution times
- Track automation rates
- Monitor customer satisfaction

## 🔧 Configuration

Key settings in `.env`:

```env
# API
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Database
DATABASE_URL=sqlite:///./tickets.db

# RAG
RAG_TOP_K=5
SIMILARITY_THRESHOLD=0.6

# Features
ENABLE_RAG=True
ENABLE_LEARNING_LOOP=True
ENABLE_ESCALATION=True
```

## 📚 Project Structure

```
├── backend/
│   ├── agents/              # Multi-agent implementations
│   │   ├── intake_agent.py
│   │   ├── classification_agent.py
│   │   ├── retrieval_agent.py
│   │   ├── response_agent.py
│   │   ├── escalation_agent.py
│   │   ├── learning_agent.py
│   │   └── orchestrator.py   # Main orchestrator
│   ├── models/              # ML models
│   │   ├── classifiers.py
│   │   └── model_manager.py
│   ├── database/            # Database layer
│   │   ├── models.py        # SQLAlchemy models
│   │   └── database.py
│   ├── rag/                 # RAG pipeline
│   │   └── rag_pipeline.py
│   ├── api/                 # FastAPI routes
│   │   ├── routes.py
│   │   ├── analytics.py
│   │   └── schemas.py
│   ├── utils/               # Utilities
│   │   ├── text_processor.py
│   │   └── embeddings.py
│   ├── config/              # Configuration
│   │   ├── settings.py
│   │   └── logger_config.py
│   └── main.py              # API server
├── frontend/
│   └── app.py               # Streamlit UI
├── data/
│   └── dataset_generator.py # Sample data
├── tests/                   # Unit tests
├── notebooks/               # Jupyter notebooks
├── requirements.txt         # Dependencies
├── .env.example             # Example env file
└── README.md               # This file
```

## 🎯 Expected Results

### System Performance
- ✅ Automatic classification (>85% accuracy)
- ✅ Sub-2 second response times
- ✅ 60-70% auto-resolution without escalation
- ✅ Intelligent escalation for complex issues

### Business Impact
- 📊 40-70% reduction in manual ticket handling
- 📈 Improved customer satisfaction scores
- ⚡ Faster resolution times
- 🔄 Continuous learning and improvement

## 🔍 Advanced Features

### RAG (Retrieval Augmented Generation)
- Searches FAQs and past tickets
- Provides context for response generation
- Improves response relevance

### Learning Loop
- Analyzes customer feedback
- Identifies improvement areas
- Suggests model retraining

### Analytics Dashboard
- Real-time metrics
- Agent performance tracking
- Customer satisfaction trends

## 📝 Example Workflow

1. **Customer submits ticket**: "My order hasn't arrived"
2. **Intake Agent**: Cleans text, extracts order ID, analyzes sentiment
3. **Classification Agent**: Categorizes as "delivery", priority "high"
4. **Retrieval Agent**: Finds similar past tickets, relevant FAQs
5. **Response Agent**: Generates personalized response with context
6. **Escalation Agent**: Evaluates if escalation needed
7. **Learning Agent**: Analyzes success for future improvement
8. **Result**: Auto-resolved or escalated to logistics team within seconds

## 🐛 Troubleshooting

**API not connecting:**
```bash
# Check if server is running
curl http://localhost:8000/health

# Check logs
tail -f logs/app_*.log
```

**Database errors:**
```bash
# Recreate tables
python -c "from backend.database import db_manager; db_manager.drop_tables(); db_manager.create_tables()"
```

**FAISS index not found:**
```bash
# Generate sample data
python data/dataset_generator.py
```

## 📖 Documentation

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Database Schema**: See `backend/database/models.py`
- **Agent Details**: See `backend/agents/` directory
- **Configuration**: Edit `.env` file

## 🚀 Deployment

### Docker Deployment
```bash
docker build -t support-ai .
docker run -p 8000:8000 -p 8501:8501 support-ai
```

### Production Deployment
1. Use PostgreSQL instead of SQLite
2. Deploy with Gunicorn/Uvicorn
3. Use Redis for caching
4. Set up monitoring and alerts
5. Configure proper logging

## 📊 Evaluation Metrics

### Classification
- Accuracy, Precision, Recall, F1-score
- Target: >85% accuracy

### Retrieval
- NDCG (Normalized Discounted Cumulative Gain)
- Mean Reciprocal Rank (MRR)

### Response Quality
- BLEU/ROUGE scores
- Human evaluation

### Operations
- Average resolution time
- Automation rate
- Escalation rate

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/name`
2. Make changes and test
3. Submit pull request
4. Ensure CI/CD passes

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Created for GUVI Project - Multi-Agent Customer Support Intelligence Platform

## 📞 Support

For issues or questions:
1. Check logs: `logs/app_*.log`
2. Review API docs: `http://localhost:8000/docs`
3. Check database: Query SQLite/PostgreSQL directly



