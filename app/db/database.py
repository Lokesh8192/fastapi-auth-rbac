from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

# Engine and session
engine = create_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
	"""Create database tables from SQLAlchemy models.

	This is a convenience for local development when migrations
	aren't applied. Prefer using Alembic migrations in production.
	"""
	Base.metadata.create_all(bind=engine)
