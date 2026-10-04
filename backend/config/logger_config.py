"""
Logger configuration
"""
import logging
import sys
import os
from loguru import logger
from datetime import datetime


def setup_logger(log_path: str = "logs", log_level: str = "INFO"):
    """Configure logger for the application"""
    
    # Remove default handler
    logger.remove()
    
    # Create logs directory if it doesn't exist
    os.makedirs(log_path, exist_ok=True)
    
    # Console handler
    logger.add(
        sys.stderr,
        format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=log_level
    )
    
    # File handler
    log_file = os.path.join(log_path, f"app_{datetime.now().strftime('%Y%m%d')}.log")
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
        rotation="500 MB",
        retention="10 days"
    )
    
    return logger
