from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

test_engine = create_engine(settings.TEST_DATABASE_URL, echo=True)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)
