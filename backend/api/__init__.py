"""__init__ file for API module"""
from .app import create_app
from .routes import router as tickets_router
from .analytics import router as analytics_router

__all__ = ["create_app", "tickets_router", "analytics_router"]
