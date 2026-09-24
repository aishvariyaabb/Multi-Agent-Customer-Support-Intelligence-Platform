"""
FastAPI routes for ticket processing
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from uuid import uuid4

from backend.api.schemas import (
    TicketCreateRequest, TicketResponse, ProcessTicketRequest,
    WorkflowResultsResponse, FeedbackRequest
)
from backend.database import Ticket, get_db, TicketStatus, TicketCategory, TicketPriority
from backend.agents.orchestrator import AgentOrchestrator
from backend.rag import RAGPipeline
from backend.config import get_settings
from loguru import logger


router = APIRouter(prefix="/api/v1", tags=["tickets"])
settings = get_settings()


# Initialize orchestrator
orchestrator = None


def get_orchestrator() -> AgentOrchestrator:
    """Get agent orchestrator instance"""
    global orchestrator
    if orchestrator is None:
        rag_pipeline = RAGPipeline(settings.faiss_index_path) if settings.rag_enabled else None
        orchestrator = AgentOrchestrator(rag_pipeline)
    return orchestrator


@router.post("/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    request: TicketCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new ticket"""
    try:
        ticket_number = f"TKT-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid4())[:8].upper()}"
        
        ticket = Ticket(
            id=str(uuid4()),
            ticket_number=ticket_number,
            customer_id=request.customer_id or f"CUST-{str(uuid4())[:8]}",
            customer_name=request.customer_name,
            customer_email=request.customer_email,
            subject=request.subject,
            description=request.description,
            category=TicketCategory.OTHER,
            priority=TicketPriority.MEDIUM,
            status=TicketStatus.OPEN,
            tags=",".join(request.tags) if request.tags else None
        )
        
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        
        logger.info(f"Ticket created: {ticket.ticket_number}")
        return ticket
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating ticket: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/process", response_model=WorkflowResultsResponse)
async def process_ticket(
    request: ProcessTicketRequest,
    db: Session = Depends(get_db)
):
    """Process ticket through multi-agent pipeline"""
    try:
        orchestrator = get_orchestrator()
        
        # Process through agents
        workflow_results = orchestrator.process_ticket(
            ticket_text=request.ticket_text,
            customer_name=request.customer_name,
            customer_email=request.customer_email,
            enable_rag=request.enable_rag,
            enable_escalation=request.enable_escalation
        )
        
        # Create ticket record in database
        ticket_number = f"TKT-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid4())[:8].upper()}"
        ticket = Ticket(
            id=str(uuid4()),
            ticket_number=ticket_number,
            customer_id=f"CUST-{str(uuid4())[:8]}",
            customer_name=request.customer_name or "Unknown",
            customer_email=request.customer_email or "unknown@example.com",
            subject=request.ticket_text[:100],
            description=request.ticket_text,
            category=getattr(TicketCategory, workflow_results.get('category', 'OTHER').upper(), TicketCategory.OTHER),
            priority=getattr(TicketPriority, workflow_results.get('priority', 'MEDIUM').upper(), TicketPriority.MEDIUM),
            status=TicketStatus.ESCALATED if workflow_results.get('requires_escalation') else TicketStatus.OPEN,
            generated_response=workflow_results.get('final_response'),
            classification_confidence=workflow_results.get('classification_confidence'),
            sentiment=workflow_results.get('sentiment'),
            requires_escalation=workflow_results.get('requires_escalation', False),
            assigned_to=workflow_results.get('assigned_team')
        )
        
        db.add(ticket)
        db.commit()
        
        logger.info(f"Ticket processed: {ticket.ticket_number}")
        
        return WorkflowResultsResponse(**workflow_results)
    
    except Exception as e:
        logger.error(f"Error processing ticket: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/tickets/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db)
):
    """Get ticket details"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    return ticket


@router.post("/tickets/{ticket_id}/feedback")
async def submit_feedback(
    ticket_id: str,
    request: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """Submit feedback for a ticket"""
    try:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found"
            )
        
        # Update ticket with feedback
        ticket.customer_satisfaction = request.rating
        ticket.feedback_text = request.feedback_text
        ticket.was_helpful = request.was_helpful
        ticket.updated_at = datetime.utcnow()
        
        db.commit()
        
        logger.info(f"Feedback submitted for ticket: {ticket.ticket_number}")
        
        return {
            "message": "Feedback received",
            "ticket_id": ticket_id,
            "rating": request.rating
        }
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
