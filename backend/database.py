from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path


# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DATABASE_DIR = Path("backend/database")

# Create database directory if it doesn't exist
DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATABASE_URL = "sqlite:///./backend/database/interview.db"


# ==========================================================
# DATABASE ENGINE
# ==========================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


# ==========================================================
# SESSION
# ==========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ==========================================================
# BASE MODEL
# ==========================================================

Base = declarative_base()


# ==========================================================
# DATABASE DEPENDENCY
# ==========================================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================================================
# CREATE DATABASE TABLES
# ==========================================================

def create_tables():
    """
    Creates all SQLAlchemy tables defined in the project.

    Existing tables are preserved.
    """

    # Import models here to ensure SQLAlchemy
    # knows about all model classes before
    # creating the tables.
    from backend import models

    Base.metadata.create_all(
        bind=engine
    )