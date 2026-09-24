"""
Pydantic schemas for API requests and responses
"""
from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class TicketCreateRequest(BaseModel):
    """Request model for creating a ticket"""
    subject: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=10)
    customer_name: str = Field(..., min_length=2)
    customer_email: EmailStr
    customer_id: Optional[str] = None
    tags: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "subject": "Order not delivered",
                "description": "My order was supposed to be delivered yesterday but I haven't received it yet",
                "customer_name": "John Doe",
                "customer_email": "john@example.com",
                "customer_id": "CUST123",
                "tags": ["delivery", "urgent"]
            }
        }


class TicketResponse(BaseModel):
    """Response model for a ticket"""
    id: str
    ticket_number: str
    customer_name: str
    customer_email: str
    subject: str
    category: Optional[str] = None
    priority: Optional[str] = None
    status: str
    generated_response: Optional[str] = None
    requires_escalation: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProcessTicketRequest(BaseModel):
    """Request model for processing a ticket

    Accepts either `ticket_text` or `description` (both are allowed).
    If `description` is provided and `ticket_text` is missing, the value
    will be used as `ticket_text` for downstream processing.
    """
    ticket_text: Optional[str] = Field(None, min_length=10)
    description: Optional[str] = Field(None, min_length=10)
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    enable_rag: bool = True
    enable_escalation: bool = True

    @model_validator(mode='before')
    def ensure_text_present(cls, values):
        ticket_text = values.get('ticket_text') if isinstance(values, dict) else None
        description = values.get('description') if isinstance(values, dict) else None
        if not ticket_text and not description:
            raise ValueError('Either `ticket_text` or `description` must be provided and have length >=10')
        # prefer ticket_text; if missing, use description
        if not ticket_text and description:
            values['ticket_text'] = description
        return values


class AgentResultResponse(BaseModel):
    """Response model for agent result"""
    agent_name: str
    status: str
    output: Dict[str, Any]
    execution_time_ms: float
    error_message: Optional[str] = None


class WorkflowResultsResponse(BaseModel):
    """Response model for complete workflow results"""
    status: str
    category: Optional[str] = None
    priority: Optional[str] = None
    sentiment: Optional[str] = None
    intent: Optional[str] = None
    final_response: Optional[str] = None
    requires_escalation: bool
    assigned_team: str
    classification_confidence: Optional[float] = None
    response_quality: Optional[float] = None
    total_execution_time_ms: float
    agent_results: Dict[str, AgentResultResponse]
    error: Optional[str] = None


class FeedbackRequest(BaseModel):
    """Request model for feedback"""
    ticket_id: str
    rating: int = Field(..., ge=1, le=5)
    feedback_text: Optional[str] = None
    was_helpful: Optional[bool] = None


class AnalyticsResponse(BaseModel):
    """Response model for analytics"""
    total_tickets: int
    auto_resolved: int
    escalated: int
    average_resolution_time_minutes: Optional[float] = None
    customer_satisfaction_score: Optional[float] = None
    classification_accuracy: Optional[float] = None
    automation_rate: float


class KnowledgeBaseItemRequest(BaseModel):
    """Request model for knowledge base item"""
    title: str = Field(..., min_length=5)
    content: str = Field(..., min_length=20)
    category: str
    tags: Optional[List[str]] = None


class KnowledgeBaseItemResponse(BaseModel):
    """Response model for knowledge base item"""
    id: str
    title: str
    content: str
    category: str
    tags: Optional[str] = None
    usage_count: int
    helpful_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True
