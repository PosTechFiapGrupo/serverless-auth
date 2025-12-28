from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from src.infrastructure.config.settings import get_settings


class DatabaseConnection:
    """
    Database connection manager using SQLAlchemy.
    
    Implements the Singleton pattern for connection pooling.
    Uses NullPool for AWS Lambda (connections don't persist).
    """
    
    _engine = None
    _session_factory = None
    
    @classmethod
    def initialize(cls):
        """Initialize database engine and session factory."""
        if cls._engine is None:
            settings = get_settings()
            
            cls._engine = create_engine(
                settings.database_url,
                poolclass=NullPool,
                echo=settings.database_echo
            )
            
            cls._session_factory = sessionmaker(
                bind=cls._engine,
                autocommit=False,
                autoflush=False
            )
    
    @classmethod
    @contextmanager
    def get_session(cls) -> Generator[Session, None, None]:
        """
        Get database session (context manager).
        
        Usage:
            with DatabaseConnection.get_session() as session:
                # use session
                pass
        """
        if cls._session_factory is None:
            cls.initialize()
        
        session = cls._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
