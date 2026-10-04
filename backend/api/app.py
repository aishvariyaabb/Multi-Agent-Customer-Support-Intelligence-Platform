"""
FastAPI application initialization and configuration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.config import get_settings, initialize_paths, setup_logger
from backend.database import db_manager
import logging


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    # Initialize settings and paths
    settings = get_settings()
    initialize_paths()
    
    # Setup logger
    logger = setup_logger(settings.logs_path, settings.log_level)
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.api_title,
        description=settings.api_description,
        version=settings.api_version,
        debug=settings.debug
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize database
    @app.on_event("startup")
    async def startup_event():
        """Initialize database on startup"""
        db_manager.create_tables()
        logger.info("Database tables initialized")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on shutdown"""
        logger.info("Application shutting down")
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": "Multi-Agent Customer Support Platform"
        }
    
    return app
