"""
Quick start guide for the Multi-Agent Customer Support Platform
"""

QUICK_START_GUIDE = """
╔════════════════════════════════════════════════════════════════╗
║   Multi-Agent Customer Support Intelligence Platform           ║
║   QUICK START GUIDE                                            ║
╚════════════════════════════════════════════════════════════════╝

📋 PREREQUISITES
─────────────────
✓ Python 3.10 or higher
✓ pip (Python package manager)
✓ ~2GB free disk space
✓ Internet connection (for model downloads on first run)

🚀 INSTALLATION (5 minutes)
───────────────────────────

Step 1: Navigate to project directory
   cd "e:\GUVI_projects\Multi-Agent Customer Support Intelligence Platform"

Step 2: Create virtual environment
   python -m venv venv
   venv\Scripts\activate

Step 3: Install dependencies
   pip install -r requirements.txt

Step 4: Initialize the system
   python setup.py

This will:
  ✓ Create .env file from template
  ✓ Create necessary directories
  ✓ Initialize database
  ✓ Generate sample datasets

🎯 RUNNING THE APPLICATION (2 terminals)
──────────────────────────────────────────

Terminal 1 - Start Backend API:
   cd backend
   python main.py
   → API starts at http://localhost:8000

Terminal 2 - Start Frontend:
   cd frontend
   streamlit run app.py
   → UI opens at http://localhost:8501

📱 ACCESSING THE SYSTEM
────────────────────────
• Frontend (Streamlit): http://localhost:8501
• API Server: http://localhost:8000
• API Docs (Swagger): http://localhost:8000/docs
• API ReDoc: http://localhost:8000/redoc

💻 FIRST TEST
──────────────
1. Open http://localhost:8501
2. Go to "New Ticket" tab
3. Fill in sample data:
   - Customer Name: John Doe
   - Email: john@example.com
   - Subject: Order not delivered
   - Description: My order ORD-123456 hasn't arrived yet
4. Click "Process Ticket"
5. Watch the agents process the ticket in real-time!

📊 EXPLORING FEATURES
──────────────────────

New Ticket Tab:
  • Submit customer support tickets
  • Watch agents process in real-time
  • View agent execution logs
  • See generated responses
  • Check escalation decisions

History Tab:
  • View all processed tickets
  • See ticket statistics
  • Track patterns
  • Analyze performance

Analytics Tab:
  • System performance metrics
  • API status
  • Processing statistics

🔧 CONFIGURATION
─────────────────
Edit .env file to configure:
  • API host/port
  • Database location
  • RAG settings
  • Feature flags
  • Logging level

📚 EXAMPLE TICKETS (for testing)
──────────────────────────────────

Delivery Issue:
  "My package hasn't arrived. Order ORD-123456 was due yesterday."

Refund Request:
  "I want to return my order. It's not what I expected."

Payment Problem:
  "I was charged twice! My card shows two charges of $99 each."

Product Issue:
  "The item arrived broken. The screen is cracked."

Account Problem:
  "I can't login to my account. Password reset isn't working."

🎯 KEY FEATURES TO TRY
──────────────────────
✓ Real-time sentiment analysis
✓ Automatic categorization
✓ Intelligent priority assignment
✓ Smart escalation
✓ Knowledge base retrieval
✓ Context-aware responses
✓ Agent execution logging
✓ Performance analytics

📈 EXPECTED PERFORMANCE
────────────────────────
• Response Time: < 2 seconds per ticket
• Classification Accuracy: > 85%
• Auto-resolution Rate: 60-70%
• Execution Time: 200-500ms per ticket

🐛 TROUBLESHOOTING
───────────────────

Issue: "API Connection Failed"
Solution:
  1. Check if backend is running: python backend/main.py
  2. Verify it's listening on http://localhost:8000/health
  3. Check firewall settings

Issue: "Module not found"
Solution:
  1. Ensure virtual environment is activated
  2. Run: pip install -r requirements.txt
  3. Check Python version: python --version

Issue: "Database error"
Solution:
  1. Delete tickets.db file
  2. Run: python setup.py
  3. Recreate database tables

Issue: "FAISS index not found"
Solution:
  Run: python data/dataset_generator.py

📚 NEXT STEPS
──────────────
1. Explore the API documentation at /docs
2. Read the README.md for detailed information
3. Check agent logs to understand processing
4. Try different ticket types
5. Monitor analytics and performance
6. Integrate with your support system

🎓 LEARNING PATH
─────────────────
1. Start with frontend UI (understand the flow)
2. Check API docs (/docs) to see endpoints
3. Review agent code in backend/agents/
4. Understand database schema in backend/database/
5. Explore RAG pipeline in backend/rag/
6. Study ML models in backend/models/

💡 TIPS FOR BEST RESULTS
─────────────────────────
• Use clear, descriptive ticket text (helps classification)
• Include relevant details (order ID, dates, etc.)
• Use realistic scenarios for testing
• Check agent logs to see how system works
• Try edge cases like very negative sentiment
• Monitor analytics to see system learning

🎉 SUCCESS INDICATORS
──────────────────────
You'll know it's working when:
✓ Tickets are categorized correctly
✓ Responses are generated within 2 seconds
✓ Simple issues are auto-resolved
✓ Complex issues escalate intelligently
✓ Analytics show high automation rate
✓ Agent logs show proper execution

📞 SUPPORT
───────────
Check the logs for detailed information:
  logs/app_*.log

Review API documentation:
  http://localhost:8000/docs

Check README.md:
  Full documentation and examples

╔════════════════════════════════════════════════════════════════╗
║   You're all set! Enjoy exploring the platform! 🚀            ║
╚════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(QUICK_START_GUIDE)
