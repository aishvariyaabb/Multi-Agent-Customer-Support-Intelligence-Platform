"""
Database operations and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
from backend.config import get_settings
from backend.database.models import Base


class DatabaseManager:
    """Database connection manager"""
    
    def __init__(self):
        self.settings = get_settings()
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def _create_engine(self):
        """Create database engine"""
        if self.settings.database_url.startswith("sqlite://"):
            # SQLite configuration
            return create_engine(
                self.settings.database_url,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=self.settings.sqlalchemy_echo
            )
        else:
            # PostgreSQL or other databases
            return create_engine(
                self.settings.database_url,
                echo=self.settings.sqlalchemy_echo,
                pool_pre_ping=True
            )
    
    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self):
        """Drop all tables (use with caution)"""
        Base.metadata.drop_all(bind=self.engine)
    
    def get_session(self) -> Generator[Session, None, None]:
        """Get database session"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


# Global database manager instance
db_manager = DatabaseManager()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for database session"""
    yield from db_manager.get_session()
