"""
Invoice Scanner: Database setup and connection
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from src.shared.config import DATABASE_URL
from src.shared.logger import logger
from src.storage_service.config import SERVICE_CONNECT_ARGS, SERVICE_SQL_ECHO

# Create database engine
# For SQLite, we use StaticPool to avoid threading issues
engine = create_engine(
    DATABASE_URL,
    connect_args=SERVICE_CONNECT_ARGS,
    poolclass=StaticPool,
    echo=SERVICE_SQL_ECHO
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

def get_db():
    """
    Dependency for getting database session
    Usage in FastAPI: def my_endpoint(db: Session = Depends(get_db))
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database, create tables"""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise