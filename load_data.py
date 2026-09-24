"""
Data Loader Script
Loads FAQ and Support Tickets from CSV files into FAISS RAG and Database
"""
import os
import sys
import csv
import pandas as pd
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.config import get_settings, initialize_paths
from backend.database import db_manager, Ticket, KnowledgeBase, TicketStatus, TicketCategory, TicketPriority
from backend.rag import RAGPipeline
from datetime import datetime
from uuid import uuid4


def load_faq_from_csv(csv_path: str) -> list:
    """Load FAQ data from CSV file"""
    print(f"\n📚 Loading FAQ Data from: {csv_path}")
    
    faqs = []
    if not os.path.exists(csv_path):
        print(f"⚠️  FAQ file not found: {csv_path}")
        return faqs
    
    try:
        df = pd.read_csv(csv_path)
        print(f"   Found {len(df)} FAQs")
        
        # Handle different column names
        question_col = None
        answer_col = None
        category_col = None
        
        for col in df.columns:
            col_lower = col.lower()
            if 'question' in col_lower or 'q' in col_lower:
                question_col = col
            elif 'answer' in col_lower or 'a' in col_lower or 'solution' in col_lower:
                answer_col = col
            elif 'category' in col_lower or 'topic' in col_lower:
                category_col = col
        
        if not question_col or not answer_col:
            print(f"   ⚠️  Required columns not found. Looking for: {df.columns.tolist()}")
            return faqs
        
        for idx, row in df.iterrows():
            faq = {
                'question': str(row[question_col]).strip(),
                'answer': str(row[answer_col]).strip(),
                'category': str(row[category_col]).strip() if category_col else 'general'
            }
            
            # Only add non-empty FAQs
            if faq['question'] and faq['answer']:
                faqs.append(faq)
        
        print(f"   ✅ Loaded {len(faqs)} valid FAQs")
        return faqs
    
    except Exception as e:
        print(f"   ❌ Error loading FAQs: {e}")
        return faqs


def load_tickets_from_csv(csv_path: str) -> list:
    """Load support tickets from CSV file"""
    print(f"\n🎫 Loading Support Tickets from: {csv_path}")
    
    tickets_data = []
    if not os.path.exists(csv_path):
        print(f"⚠️  Tickets file not found: {csv_path}")
        return tickets_data
    
    try:
        df = pd.read_csv(csv_path)
        print(f"   Found {len(df)} tickets")
        
        # Auto-detect columns
        subject_col = None
        description_col = None
        category_col = None
        status_col = None
        customer_col = None
        email_col = None
        
        for col in df.columns:
            col_lower = col.lower()
            if 'subject' in col_lower or 'issue' in col_lower or 'title' in col_lower:
                subject_col = col
            # Also accept common alternate names used in provided CSVs
            elif 'description' in col_lower or 'details' in col_lower or 'message' in col_lower or 'ticket_text' in col_lower or 'ticket' in col_lower and 'text' in col_lower:
                description_col = col
            elif 'category' in col_lower or 'type' in col_lower or 'ticket_category' in col_lower:
                category_col = col
            elif 'status' in col_lower:
                status_col = col
            elif 'customer' in col_lower or 'name' in col_lower:
                customer_col = col
            elif 'email' in col_lower:
                email_col = col
        
        print(f"   Detected columns: subject={subject_col}, description={description_col}, category={category_col}")
        
        for idx, row in df.iterrows():
            try:
                ticket = {
                    'subject': str(row[subject_col]).strip() if subject_col else f"Ticket {idx}",
                    'description': str(row[description_col]).strip() if description_col else "",
                    'category': str(row[category_col]).strip() if category_col else 'other',
                    'status': str(row[status_col]).strip() if status_col else 'open',
                    'customer_name': str(row[customer_col]).strip() if customer_col else f"Customer {idx}",
                    'customer_email': str(row[email_col]).strip() if email_col else f"customer{idx}@example.com"
                }
                
                if ticket['description']:
                    tickets_data.append(ticket)
            except Exception as e:
                print(f"   ⚠️  Error processing row {idx}: {e}")
                continue
        
        print(f"   ✅ Loaded {len(tickets_data)} valid tickets")
        return tickets_data
    
    except Exception as e:
        print(f"   ❌ Error loading tickets: {e}")
        return tickets_data


def populate_rag_pipeline(faq_list: list, ticket_list: list):
    """Populate RAG pipeline with FAQ and ticket data"""
    print("\n🔍 Populating RAG Pipeline...")
    
    settings = get_settings()
    rag_pipeline = RAGPipeline(settings.faiss_index_path)
    
    # Add FAQs
    if faq_list:
        print(f"   Adding {len(faq_list)} FAQs to RAG...")
        rag_pipeline.add_faq_documents(faq_list)
        print(f"   ✅ FAQs added to RAG")
    
    # Add past tickets
    if ticket_list:
        past_tickets = []
        for ticket in ticket_list[:1000]:  # Limit to 1000 for performance
            past_tickets.append({
                'title': ticket['subject'],
                'description': ticket['description'],
                'resolution': f"Previously resolved: {ticket['subject']}",
                'category': ticket['category']
            })
        
        if past_tickets:
            print(f"   Adding {len(past_tickets)} past tickets to RAG...")
            rag_pipeline.add_past_tickets(past_tickets)
            print(f"   ✅ Past tickets added to RAG")
    
    # Show stats
    stats = rag_pipeline.get_stats()
    print(f"\n   RAG Pipeline Stats:")
    print(f"      Total documents: {stats['total_documents']}")
    print(f"      Embedding dimension: {stats['embedding_dimension']}")
    
    return rag_pipeline


def populate_database(faq_list: list, ticket_list: list):
    """Populate database with FAQ and ticket data"""
    print("\n💾 Populating Database...")
    
    db_manager.create_tables()
    
    # Insert FAQs into knowledge base
    with next(db_manager.get_session()) as db:
        existing_faqs = db.query(KnowledgeBase).count()
        
        if existing_faqs == 0 and faq_list:
            print(f"   Adding {len(faq_list)} FAQs to database...")
            for faq in faq_list[:500]:  # Limit to 500 for performance
                kb_item = KnowledgeBase(
                    id=str(uuid4()),
                    title=faq['question'],
                    content=faq['answer'],
                    category=faq['category'],
                    tags=faq['category'],
                    is_active=True
                )
                db.add(kb_item)
            
            db.commit()
            print(f"   ✅ FAQs added to database")
        else:
            print(f"   ℹ️  Database already has {existing_faqs} FAQs, skipping")
    
    # Insert sample tickets for analysis
    with next(db_manager.get_session()) as db:
        existing_tickets = db.query(Ticket).count()
        
        if existing_tickets == 0 and ticket_list:
            print(f"   Adding {len(ticket_list[:100])} sample tickets to database...")
            
            category_map = {
                'delivery': TicketCategory.DELIVERY,
                'refund': TicketCategory.REFUND,
                'payment': TicketCategory.PAYMENT,
                'product': TicketCategory.PRODUCT_ISSUE,
                'order': TicketCategory.ORDER_TRACKING,
                'account': TicketCategory.ACCOUNT,
            }
            
            for ticket in ticket_list[:100]:
                # Normalize incoming category text to the TicketCategory enum values
                incoming_cat = (ticket.get('category') or 'other')
                cat_lower = incoming_cat.lower()

                if 'refund' in cat_lower:
                    category = TicketCategory.REFUND
                elif 'payment' in cat_lower or 'emi' in cat_lower:
                    category = TicketCategory.PAYMENT
                elif 'delivery' in cat_lower or 'deliv' in cat_lower:
                    category = TicketCategory.DELIVERY
                elif 'product' in cat_lower or 'issue' in cat_lower or 'product_issue' in cat_lower:
                    category = TicketCategory.PRODUCT_ISSUE
                elif 'order' in cat_lower or 'tracking' in cat_lower:
                    category = TicketCategory.ORDER_TRACKING
                elif 'account' in cat_lower or 'login' in cat_lower:
                    category = TicketCategory.ACCOUNT
                else:
                    category = TicketCategory.OTHER
                
                new_ticket = Ticket(
                    id=str(uuid4()),
                    ticket_number=f"TKT-{datetime.now().strftime('%Y%m%d')}-{str(uuid4())[:8].upper()}",
                    customer_id=f"CUST-{str(uuid4())[:8]}",
                    customer_name=ticket['customer_name'],
                    customer_email=ticket['customer_email'],
                    subject=ticket['subject'][:255],
                    description=ticket['description'],
                    category=category,
                    priority=TicketPriority.MEDIUM,
                    status=TicketStatus.OPEN,
                    is_automated=True
                )
                db.add(new_ticket)
            
            db.commit()
            print(f"   ✅ Sample tickets added to database")
        else:
            print(f"   ℹ️  Database already has {existing_tickets} tickets, skipping")

    # After inserting tickets, attempt to train classifiers if we have data
    try:
        from backend.models import get_model_manager
        from backend.database import Ticket as TicketModel

        with next(db_manager.get_session()) as db:
            tickets_for_training = db.query(TicketModel).all()

        texts = [t.description for t in tickets_for_training if t.description]
        labels = []
        for t in tickets_for_training:
            cat = getattr(t, 'category', None)
            # category may be enum or string
            cat_str = cat.value if hasattr(cat, 'value') else str(cat)
            cat_lower = (cat_str or '').lower()

            if 'refund' in cat_lower:
                labels.append('refund')
            elif 'payment' in cat_lower:
                labels.append('payment')
            elif 'delivery' in cat_lower:
                labels.append('delivery')
            elif 'product' in cat_lower or 'issue' in cat_lower:
                labels.append('product_issue')
            elif 'order' in cat_lower or 'tracking' in cat_lower:
                labels.append('order_tracking')
            elif 'account' in cat_lower:
                labels.append('account')
            else:
                labels.append('other')

        # Only train if we have at least some labeled examples
        if len(texts) >= 10 and len(texts) == len(labels):
            print("\n🔧 Training category classifier on loaded tickets...")
            mm = get_model_manager()
            try:
                mm.category_classifier.train(texts, labels)
                mm.save_models()
                print("   ✅ Category classifier trained and saved")
            except Exception as e:
                print(f"   ⚠️  Error training classifier: {e}")
        else:
            print("\n⚠️  Not enough ticket data to train classifier (need >=10). Skipping training.")
    except Exception as e:
        print(f"\n⚠️  Skipping training due to error: {e}")


def main():
    """Main function"""
    print("="*70)
    print("🚀 DATA LOADER - Multi-Agent Support Platform")
    print("="*70)
    
    # Initialize
    initialize_paths()
    settings = get_settings()
    
    # Find CSV files
    project_root = Path(__file__).parent
    faq_file = None
    tickets_file = None
    
    # Search for FAQ file
    for pattern in ['faq*.csv', '*faq*.csv', '*knowledge*.csv']:
        matches = list(project_root.glob(pattern))
        if matches:
            faq_file = str(matches[0])
            break
    
    # Search for tickets file
    for pattern in ['*ticket*.csv', '*support*.csv', '*10k*.csv']:
        matches = list(project_root.glob(pattern))
        if matches:
            tickets_file = str(matches[0])
            break
    
    print(f"\n📁 Looking for data files...")
    print(f"   FAQ file: {faq_file if faq_file else '❌ Not found'}")
    print(f"   Tickets file: {tickets_file if tickets_file else '❌ Not found'}")
    
    # Load data
    faq_list = []
    ticket_list = []
    
    if faq_file:
        faq_list = load_faq_from_csv(faq_file)
    
    if tickets_file:
        ticket_list = load_tickets_from_csv(tickets_file)
    
    # Populate systems
    if faq_list or ticket_list:
        populate_rag_pipeline(faq_list, ticket_list)
        populate_database(faq_list, ticket_list)
        
        print("\n✅ Data Loading Complete!")
        print(f"\n📊 Summary:")
        print(f"   FAQs loaded: {len(faq_list)}")
        print(f"   Tickets loaded: {len(ticket_list)}")
        print(f"   RAG index created")
        print(f"   Database populated")
    else:
        print("\n⚠️  No data files found or loaded")
    
    print("\n" + "="*70)
    print("Ready to start the application!")
    print("="*70)


if __name__ == "__main__":
    main()
