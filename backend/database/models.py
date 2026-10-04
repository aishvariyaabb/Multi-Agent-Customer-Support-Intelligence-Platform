"""
Database models for customer support system
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from uuid import uuid4

Base = declarative_base()


class TicketStatus(str, enum.Enum):
    """Ticket status enumeration"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    CLOSED = "closed"


class TicketPriority(str, enum.Enum):
    """Ticket priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TicketCategory(str, enum.Enum):
    """Ticket category enumeration"""
    DELIVERY = "delivery"
    REFUND = "refund"
    PAYMENT = "payment"
    PRODUCT_ISSUE = "product_issue"
    ORDER_TRACKING = "order_tracking"
    ACCOUNT = "account"
    OTHER = "other"


class Sentiment(str, enum.Enum):
    """Sentiment enumeration"""
    VERY_NEGATIVE = "very_negative"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"
    VERY_POSITIVE = "very_positive"


class Ticket(Base):
    """Ticket model"""
    __tablename__ = "tickets"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    ticket_number = Column(String(20), unique=True, nullable=False, index=True)
    customer_id = Column(String(50), nullable=False, index=True)
    customer_name = Column(String(100), nullable=False)
    customer_email = Column(String(100), nullable=False)
    
    # Ticket Content
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    
    # Classification
    category = Column(Enum(TicketCategory), nullable=False, index=True)
    priority = Column(Enum(TicketPriority), nullable=False, index=True)
    sentiment = Column(Enum(Sentiment), nullable=True)
    
    # Agent Results
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN, index=True)
    assigned_to = Column(String(100), nullable=True)
    generated_response = Column(Text, nullable=True)
    
    # Confidence Scores
    classification_confidence = Column(Float, nullable=True)
    sentiment_confidence = Column(Float, nullable=True)
    response_quality_score = Column(Float, nullable=True)
    
    # RAG/Retrieval Information
    retrieved_documents_count = Column(Integer, default=0)
    retrieval_confidence = Column(Float, nullable=True)
    
    # Flags
    requires_escalation = Column(Boolean, default=False)
    escalation_reason = Column(String(500), nullable=True)
    is_automated = Column(Boolean, default=True)
    
    # Feedback
    customer_satisfaction = Column(Integer, nullable=True)  # 1-5 scale
    feedback_text = Column(Text, nullable=True)
    was_helpful = Column(Boolean, nullable=True)
    
    # Metadata
    resolution_time_minutes = Column(Integer, nullable=True)
    follow_up_required = Column(Boolean, default=False)
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Ticket(id={self.id}, ticket_number={self.ticket_number}, status={self.status})>"


class AgentLog(Base):
    """Agent execution logs"""
    __tablename__ = "agent_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    ticket_id = Column(String(36), nullable=False, index=True)
    agent_name = Column(String(50), nullable=False, index=True)
    agent_role = Column(String(50), nullable=False)
    
    # Execution Details
    input_data = Column(Text, nullable=False)  # JSON
    output_data = Column(Text, nullable=True)  # JSON
    execution_time_ms = Column(Integer, nullable=True)
    
    # Status
    status = Column(String(20), nullable=False)  # success, error, skipped
    error_message = Column(Text, nullable=True)
    
    # Metadata
    execution_order = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<AgentLog(ticket_id={self.ticket_id}, agent={self.agent_name}, status={self.status})>"


class RetrievedDocument(Base):
    """Retrieved documents from RAG"""
    __tablename__ = "retrieved_documents"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    ticket_id = Column(String(36), nullable=False, index=True)
    
    # Document Info
    document_type = Column(String(50), nullable=False)  # faq, past_ticket, kb_article
    document_id = Column(String(100), nullable=False)
    document_title = Column(String(255), nullable=True)
    document_content = Column(Text, nullable=False)
    
    # Similarity
    similarity_score = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<RetrievedDocument(ticket_id={self.ticket_id}, type={self.document_type}, score={self.similarity_score})>"


class FeedbackLog(Base):
    """Customer feedback and corrections"""
    __tablename__ = "feedback_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    ticket_id = Column(String(36), nullable=False, index=True)
    
    # Feedback
    agent_response = Column(Text, nullable=False)
    customer_feedback = Column(Text, nullable=False)
    corrected_response = Column(Text, nullable=True)
    
    # Rating
    response_quality_rating = Column(Integer, nullable=True)  # 1-5
    was_issue_resolved = Column(Boolean, nullable=True)
    requires_escalation = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    feedback_source = Column(String(50), nullable=True)  # customer, system, admin
    
    def __repr__(self):
        return f"<FeedbackLog(ticket_id={self.ticket_id}, rating={self.response_quality_rating})>"


class PerformanceMetric(Base):
    """System performance metrics"""
    __tablename__ = "performance_metrics"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    
    # Time-based metrics
    metric_date = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Classification Metrics
    classification_accuracy = Column(Float, nullable=True)
    classification_precision = Column(Float, nullable=True)
    classification_recall = Column(Float, nullable=True)
    classification_f1_score = Column(Float, nullable=True)
    
    # Sentiment Metrics
    sentiment_accuracy = Column(Float, nullable=True)
    
    # Retrieval Metrics
    retrieval_mean_reciprocal_rank = Column(Float, nullable=True)
    retrieval_ndcg_score = Column(Float, nullable=True)
    
    # Response Metrics
    response_bleu_score = Column(Float, nullable=True)
    response_rouge_score = Column(Float, nullable=True)
    response_human_evaluation = Column(Float, nullable=True)
    
    # Operational Metrics
    avg_resolution_time_minutes = Column(Float, nullable=True)
    automation_rate = Column(Float, nullable=True)
    escalation_rate = Column(Float, nullable=True)
    customer_satisfaction_score = Column(Float, nullable=True)
    
    # Volume Metrics
    total_tickets_processed = Column(Integer, default=0)
    auto_resolved_count = Column(Integer, default=0)
    escalated_count = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<PerformanceMetric(date={self.metric_date}, satisfaction={self.customer_satisfaction_score})>"


class KnowledgeBase(Base):
    """Knowledge base articles and FAQs"""
    __tablename__ = "knowledge_base"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    
    # Content
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    tags = Column(String(500), nullable=True)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    usage_count = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)
    unhelpful_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<KnowledgeBase(id={self.id}, title={self.title})>"
