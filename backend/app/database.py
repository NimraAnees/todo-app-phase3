"""
Database connection and session management for SQLModel.

Provides:
- SQLModel engine configuration
- Session factory for database operations
- get_db() dependency for FastAPI dependency injection
"""
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from app.core.config import settings


# Create SQLModel engine with PostgreSQL connection
# echo=True enables SQL query logging (useful for development, disable in production)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,  # Number of connections to maintain
    max_overflow=10,  # Maximum overflow connections beyond pool_size
)


def create_db_and_tables():
    """
    Create all database tables defined in SQLModel models.

    Called during application startup to ensure database schema exists.
    Uses SQLModel.metadata.create_all() to generate CREATE TABLE statements.

    Warning:
        This is a simple approach suitable for development.
        For production, use proper migrations (Alembic) to manage schema changes.
    """
    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    Yields a SQLModel Session for the duration of the request.
    Automatically commits on success and rolls back on exception.
    Always closes the session after the request completes.

    Usage:
        @app.get("/users")
        async def get_users(db: Session = Depends(get_db)):
            users = db.exec(select(User)).all()
            return users

    Yields:
        Session: SQLModel database session for executing queries

    Example:
        def get_user_by_email(db: Session, email: str) -> User | None:
            statement = select(User).where(User.email == email)
            return db.exec(statement).first()
    """
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
