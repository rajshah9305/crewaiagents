from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.config import settings

# Optimized database configuration
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,                    # Number of persistent connections
    max_overflow=30,                 # Additional connections when needed
    pool_pre_ping=True,              # Validate connections before use
    pool_recycle=3600,               # Recycle connections every hour
    echo=False,                      # Disable SQL logging in production
    future=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False           # Prevent expired object issues
)

Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    from app.models import user, agent, conversation, workflow
    Base.metadata.create_all(bind=engine) 