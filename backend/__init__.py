"""__init__ file for backend module"""
__version__ = "1.0.0"
__author__ = "GUVI Support"

from backend.config import get_settings, initialize_paths, setup_logger
from backend.database import db_manager, get_db

# Initialize on import
initialize_paths()

__all__ = ["get_settings", "initialize_paths", "setup_logger", "db_manager", "get_db"]
