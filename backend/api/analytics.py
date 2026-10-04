"""
FastAPI routes for analytics and monitoring
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from backend.api.schemas import AnalyticsResponse
from backend.database import Ticket, TicketStatus, PerformanceMetric, get_db
from loguru import logger


router = APIRouter(prefix="/api/v1", tags=["analytics"])


@router.get("/analytics/overview", response_model=AnalyticsResponse)
async def get_analytics_overview(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """Get analytics overview for the last N days"""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Count total tickets
        total_tickets = db.query(func.count(Ticket.id)).filter(
            Ticket.created_at >= start_date
        ).scalar()
        
        # Count auto-resolved tickets
        auto_resolved = db.query(func.count(Ticket.id)).filter(
            Ticket.created_at >= start_date,
            Ticket.is_automated == True,
            Ticket.status == TicketStatus.RESOLVED
        ).scalar()
        
        # Count escalated tickets
        escalated = db.query(func.count(Ticket.id)).filter(
            Ticket.created_at >= start_date,
            Ticket.requires_escalation == True
        ).scalar()
        
        # Calculate automation rate
        automation_rate = (auto_resolved / total_tickets * 100) if total_tickets > 0 else 0
        
        # Get average resolution time
        avg_resolution_time = None
        resolved_tickets = db.query(func.avg(Ticket.resolution_time_minutes)).filter(
            Ticket.created_at >= start_date,
            Ticket.resolution_time_minutes.isnot(None)
        ).scalar()
        if resolved_tickets:
            avg_resolution_time = float(resolved_tickets)
        
        # Get customer satisfaction score
        satisfaction_score = None
        avg_satisfaction = db.query(func.avg(Ticket.customer_satisfaction)).filter(
            Ticket.created_at >= start_date,
            Ticket.customer_satisfaction.isnot(None)
        ).scalar()
        if avg_satisfaction:
            satisfaction_score = float(avg_satisfaction)
        
        logger.info(f"Analytics generated for last {days} days")
        
        return AnalyticsResponse(
            total_tickets=total_tickets,
            auto_resolved=auto_resolved,
            escalated=escalated,
            average_resolution_time_minutes=avg_resolution_time,
            customer_satisfaction_score=satisfaction_score,
            classification_accuracy=None,
            automation_rate=automation_rate
        )
    
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/analytics/tickets/by-category")
async def get_tickets_by_category(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """Get ticket distribution by category"""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        results = db.query(
            Ticket.category,
            func.count(Ticket.id).label('count')
        ).filter(
            Ticket.created_at >= start_date
        ).group_by(Ticket.category).all()
        
        return {
            "data": [{"category": cat, "count": count} for cat, count in results],
            "period_days": days
        }
    
    except Exception as e:
        logger.error(f"Error getting tickets by category: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/analytics/tickets/by-priority")
async def get_tickets_by_priority(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """Get ticket distribution by priority"""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        results = db.query(
            Ticket.priority,
            func.count(Ticket.id).label('count')
        ).filter(
            Ticket.created_at >= start_date
        ).group_by(Ticket.priority).all()
        
        return {
            "data": [{"priority": priority, "count": count} for priority, count in results],
            "period_days": days
        }
    
    except Exception as e:
        logger.error(f"Error getting tickets by priority: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
