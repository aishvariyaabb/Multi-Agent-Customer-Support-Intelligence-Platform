"""
Configuration module for the Multi-Agent Customer Support Platform
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional
import os
from pathlib import Path
from pydantic import Field, AliasChoices


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    """Application settings"""
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )

    # FastAPI
    api_host: str = "0.0.0.0"
    api_port: int = Field(
        default=8015,
        validation_alias=AliasChoices("API_PORT", "FASTAPI_PORT", "api_port", "FASTAPI_API_PORT"),
    )
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
    # API-key based LLM only. No local fallback, no default OpenAI model.
    openai_api_key: Optional[str] = None
    openai_model: Optional[str] = None
    openai_base_url: Optional[str] = None
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

    @property
    def llm_ready(self) -> bool:
        """Return True only when the API-key-based Gemini config is complete."""
        key = (self.openai_api_key or '').strip()
        invalid = {"", "abcd", "test", "demo", "example", "placeholder", "your_api_key_here", "ollama", "openai"}
        if key.lower() in invalid:
            return False
        return bool(self.openai_api_key and self.openai_model and self.openai_base_url)

    def validate_llm_settings(self):
        """Raise a clear error if the app is missing a valid API-backed LLM configuration."""
        if not self.llm_ready:
            raise ValueError(
                "LLM configuration is invalid. Set OPENAI_API_KEY, OPENAI_MODEL, and OPENAI_BASE_URL to a valid Gemini API configuration. "
                "This app does not support local or default fallback values."
            )


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
