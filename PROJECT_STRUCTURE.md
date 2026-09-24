"""
Project Structure Visualization
"""

STRUCTURE = """
╔════════════════════════════════════════════════════════════════════════════╗
║  Multi-Agent Customer Support Intelligence Platform - Project Structure    ║
╚════════════════════════════════════════════════════════════════════════════╝

📦 PROJECT ROOT
│
├── 📁 backend/                    ← Core Backend Services
│   ├── 🤖 agents/                 ← Multi-Agent System
│   │   ├── base_agent.py
│   │   ├── intake_agent.py        ← Text Processing & Entity Extraction
│   │   ├── classification_agent.py ← Category & Priority Assignment  
│   │   ├── retrieval_agent.py     ← RAG-based Knowledge Retrieval
│   │   ├── response_agent.py      ← Contextual Response Generation
│   │   ├── escalation_agent.py    ← Smart Routing & Escalation
│   │   ├── learning_agent.py      ← System Learning & Improvement
│   │   ├── orchestrator.py        ← Agent Workflow Coordinator
│   │   └── __init__.py
│   │
│   ├── 🧠 models/                 ← ML Models & Classifiers
│   │   ├── classifiers.py         ← Category, Priority, Intent
│   │   ├── model_manager.py       ← Model Lifecycle Management
│   │   └── __init__.py
│   │
│   ├── 🗄️  database/              ← Data Layer
│   │   ├── models.py              ← SQLAlchemy ORM Models
│   │   ├── database.py            ← Database Connection Manager
│   │   └── __init__.py
│   │
│   ├── 🔍 rag/                    ← Retrieval Augmented Generation
│   │   ├── rag_pipeline.py        ← FAISS Vector Search Pipeline
│   │   └── __init__.py
│   │
│   ├── ⚙️  api/                   ← FastAPI Backend
│   │   ├── app.py                 ← FastAPI Application Setup
│   │   ├── routes.py              ← Ticket Processing Routes
│   │   ├── analytics.py           ← Analytics Endpoints
│   │   ├── schemas.py             ← Pydantic Models
│   │   └── __init__.py
│   │
│   ├── 🛠️  utils/                 ← Utility Functions
│   │   ├── text_processor.py      ← Text Cleaning & NLP
│   │   ├── embeddings.py          ← Text Embedding Management
│   │   └── __init__.py
│   │
│   ├── ⚙️  config/                ← Configuration Management
│   │   ├── settings.py            ← Application Settings
│   │   ├── logger_config.py       ← Logging Configuration
│   │   └── __init__.py
│   │
│   ├── main.py                    ← API Server Entry Point
│   └── __init__.py
│
├── 📁 frontend/                   ← Streamlit UI
│   └── app.py                     ← Interactive Web Dashboard
│
├── 📁 data/                       ← Data & Datasets
│   └── dataset_generator.py      ← Sample Data Generator
│
├── 📁 notebooks/                  ← Jupyter Notebooks
│   └── demo.ipynb                ← Interactive Demo
│
├── 📁 tests/                      ← Unit & Integration Tests
│   (test files to be added)
│
├── 📁 logs/                       ← Application Logs
│   (generated automatically)
│
├── 🚀 run_all.py                 ← Start All Services Script
├── ✅ validate.py                 ← Project Validation Script
├── 🔧 setup.py                    ← Windows Setup Script
├── 🔧 setup.sh                    ← macOS/Linux Setup Script
│
├── 📋 README.md                   ← Full Documentation
├── 🚀 QUICK_START.md              ← Quick Start Guide
├── 📦 requirements.txt            ← Dependencies
├── .env                           ← Environment Variables
├── .env.example                   ← Environment Template
├── .gitignore                     ← Git Ignore Rules
│
└── 📄 PROJECT_STRUCTURE.txt       ← This File


════════════════════════════════════════════════════════════════════════════

🎯 AGENT WORKFLOW FLOW

┌─────────────────────────────────────────────────────────────┐
│ User Submit Ticket (Streamlit UI / API)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴────────────┐
         │   AGENT ORCHESTRATOR   │
         └───────────┬────────────┘
                     │
         ┌───────────▼────────────────────┐
         │ 1️⃣  INTAKE AGENT              │
         │  • Clean Text                  │
         │  • Extract Entities            │
         │  • Analyze Sentiment           │
         └───────────┬────────────────────┘
                     │
         ┌───────────▼────────────────────┐
         │ 2️⃣  CLASSIFICATION AGENT      │
         │  • Predict Category            │
         │  • Assign Priority             │
         │  • Extract Intent              │
         └───────────┬────────────────────┘
                     │
         ┌───────────▼────────────────────┐
         │ 3️⃣  RETRIEVAL AGENT (RAG)     │
         │  • Search Knowledge Base       │
         │  • Retrieve FAQ/Past Tickets   │
         │  • Generate Context            │
         └───────────┬────────────────────┘
                     │
         ┌───────────▼────────────────────┐
         │ 4️⃣  RESPONSE AGENT            │
         │  • Generate Response           │
         │  • Personalize Message         │
         │  • Calculate Quality Score     │
         └───────────┬────────────────────┘
                     │
         ┌───────────▼────────────────────┐
         │ 5️⃣  ESCALATION AGENT          │
         │  • Evaluate Escalation Need    │
         │  • Assign Team                 │
         │  • Set Priority Level          │
         └───────────┬────────────────────┘
                     │
         ┌───────────▼────────────────────┐
         │ 6️⃣  LEARNING AGENT            │
         │  • Analyze Outcomes            │
         │  • Extract Insights            │
         │  • Record for Improvement      │
         └───────────┬────────────────────┘
                     │
       ┌─────────────▼─────────────┐
       │   Result Stored in DB     │
       │   Response to User         │
       └───────────────────────────┘


════════════════════════════════════════════════════════════════════════════

💾 DATABASE SCHEMA

┌─────────────────────────────────────────────────────────────┐
│ TICKETS TABLE                                               │
├─────────────────────────────────────────────────────────────┤
│ • id (PK)                                                   │
│ • ticket_number                                             │
│ • customer_id, customer_name, customer_email                │
│ • subject, description                                      │
│ • category, priority, sentiment, status                     │
│ • generated_response                                        │
│ • classification_confidence, sentiment_confidence           │
│ • requires_escalation, assigned_to                          │
│ • customer_satisfaction, feedback_text, was_helpful         │
│ • created_at, updated_at, resolved_at                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ AGENT_LOGS TABLE     │ RETRIEVED_DOCUMENTS TABLE            │
├─────────────────────┼──────────────────────────────────────┤
│ • id (PK)           │ • id (PK)                            │
│ • ticket_id (FK)    │ • ticket_id (FK)                     │
│ • agent_name        │ • document_type                      │
│ • input_data        │ • document_id                        │
│ • output_data       │ • similarity_score                   │
│ • execution_time    │ • rank                              │
│ • status            │ • created_at                         │
│ • timestamp         │                                      │
└─────────────────────┴──────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ FEEDBACK_LOGS TABLE                                          │
├──────────────────────────────────────────────────────────────┤
│ • id (PK)                                                    │
│ • ticket_id (FK)                                             │
│ • agent_response, customer_feedback, corrected_response      │
│ • response_quality_rating, was_issue_resolved                │
│ • created_at, feedback_source                                │
└──────────────────────────────────────────────────────────────┘


════════════════════════════════════════════════════════════════════════════

🔗 API ENDPOINTS

POST /api/v1/process
  └─ Process ticket through multi-agent pipeline

POST /api/v1/tickets
  └─ Create new ticket

GET /api/v1/tickets/{id}
  └─ Get ticket details

POST /api/v1/tickets/{id}/feedback
  └─ Submit customer feedback

GET /api/v1/analytics/overview
  └─ Get system analytics

GET /api/v1/analytics/tickets/by-category
  └─ Get category distribution

GET /api/v1/analytics/tickets/by-priority
  └─ Get priority distribution


════════════════════════════════════════════════════════════════════════════

🛠️  TECH STACK SUMMARY

Backend:
  • FastAPI (REST API)
  • SQLAlchemy (ORM)
  • SQLite/PostgreSQL (Database)
  • Python 3.10+

Frontend:
  • Streamlit (Web UI)
  • Plotly (Visualizations)

AI/ML:
  • Scikit-learn (Classification)
  • HuggingFace (NLP)
  • Sentence-Transformers (Embeddings)
  • FAISS (Vector Search)

Agent Orchestration:
  • LangChain / CrewAI
  • Custom Agent Framework

Utilities:
  • Pandas, NumPy (Data Processing)
  • Loguru (Logging)
  • Pydantic (Validation)


════════════════════════════════════════════════════════════════════════════

🎯 KEY FEATURES

✨ Multi-Agent System
  └─ 6 specialized agents working together

🧠 Intelligent Classification  
  └─ Auto-categorize and prioritize tickets

🔍 RAG Integration
  └─ Knowledge base retrieval with FAISS

📊 Real-time Analytics
  └─ Track system performance metrics

🚨 Smart Escalation
  └─ Intelligent routing to teams

🔄 Learning Loop
  └─ Continuous improvement from feedback

💬 Streamlit Interface
  └─ Chat-based support dashboard

📈 Performance Tracking
  └─ Comprehensive metrics and logging

════════════════════════════════════════════════════════════════════════════

For detailed information, see README.md
For quick start guide, see QUICK_START.md
"""

if __name__ == "__main__":
    print(STRUCTURE)
