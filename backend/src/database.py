from sqlmodel import create_engine, Session
from sqlalchemy import event
from sqlalchemy.pool import Pool
from .config.settings import settings
from .models import User, Task, Conversation, Message, ToolCall


# Create engine with connection pooling
engine = create_engine(
    settings.database_url,
    echo=False,  # Set to True for SQL debug output
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    pool_size=20,        # Number of connection objects to maintain
    max_overflow=30,     # Additional connections beyond pool_size
    connect_args={
        "application_name": "ai_chat_agent",  # Application name for monitoring
    }
)


def get_session():
    """
    Get a database session for dependency injection.

    Yields:
        Session: Database session instance
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """
    Create database tables based on SQLModel models.
    This should be called when starting the application.
    """
    from sqlmodel import SQLModel

    # Create all tables
    SQLModel.metadata.create_all(engine)


# Optional: Add connection event listeners for monitoring
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Set SQLite pragmas for better performance (only needed for SQLite).
    For PostgreSQL, this won't have effect.
    """
    if 'sqlite' in settings.database_url:
        cursor = dbapi_connection.cursor()
        # Use WAL mode for better concurrency
        cursor.execute("PRAGMA journal_mode=WAL")
        # Synchronous NORMAL for balance of safety and performance
        cursor.execute("PRAGMA synchronous=NORMAL")
        # Increase cache size
        cursor.execute("PRAGMA cache_size=10000")
        cursor.close()


def get_engine():
    """
    Get the database engine instance.

    Returns:
        Engine: SQLAlchemy engine instance
    """
    return engine