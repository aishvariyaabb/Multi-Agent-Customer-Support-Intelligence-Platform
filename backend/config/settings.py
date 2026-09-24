"""
Configuration module for the Multi-Agent Customer Support Platform
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # FastAPI
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "Multi-Agent Customer Support Platform"
    api_version: str = "1.0.0"
    api_description: str = "Intelligent ticket management system with multi-agent orchestration"
    debug: bool = False
    secret_key: str = "your-secret-key-change-in-production"
    
    # Paths
    data_path: str = "./data"
    models_path: str = "./backend/models"
    logs_path: str = "./logs"
    faiss_index_path: str = "./data/faiss_index"
    
    # Database
    database_url: str = "sqlite:///./tickets.db"
    sqlalchemy_echo: bool = False
    mongodb_url: Optional[str] = None
    mongodb_database: str = "customer_support"
    
    # LLM Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    openai_temperature: float = 0.7
    
    # RAG Configuration
    rag_enabled: bool = True
    rag_top_k: int = 5
    similarity_threshold: float = 0.6
    vector_db_type: str = "faiss"
    
    # System Features
    learning_loop_enabled: bool = True
    escalation_enabled: bool = True
    analytics_enabled: bool = True
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # Cache
    redis_url: Optional[str] = None
    cache_ttl: int = 3600
    
    # Email Configuration
    smtp_server: Optional[str] = None
    smtp_port: int = 587
    sender_email: Optional[str] = None
    sender_password: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get application settings"""
    return Settings()


# Create necessary directories if they don't exist
def initialize_paths():
    """Initialize required directories"""
    settings = get_settings()
    for path in [settings.data_path, settings.models_path, settings.logs_path]:
        os.makedirs(path, exist_ok=True)
