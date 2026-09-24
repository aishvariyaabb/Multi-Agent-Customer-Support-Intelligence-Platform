"""
Main FastAPI server entry point
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import uvicorn
from backend.api import create_app, tickets_router, analytics_router
from backend.config import get_settings
from loguru import logger

# Create app
app = create_app()

# Include routers
app.include_router(tickets_router)
app.include_router(analytics_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Multi-Agent Customer Support Intelligence Platform",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    settings = get_settings()
    logger.info(f"Starting server on {settings.api_host}:{settings.api_port}")
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower()
    )
