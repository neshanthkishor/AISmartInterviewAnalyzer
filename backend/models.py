from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.sql import func

from backend.database import Base


# ==========================================================
# USER MODEL
# ==========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        index=True,
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# ==========================================================
# INTERVIEW MODEL
# ==========================================================

class Interview(Base):
    """
    Stores completed AI interview sessions.

    Each interview belongs to one registered user.
    """

    __tablename__ = "interviews"

    # ------------------------------------------------------
    # PRIMARY KEY
    # ------------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ------------------------------------------------------
    # USER RELATION
    # ------------------------------------------------------

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # ------------------------------------------------------
    # INTERVIEW CONFIGURATION
    # ------------------------------------------------------

    interview_type = Column(
        String(50),
        nullable=False,
        default="Technical"
    )

    role = Column(
        String(100),
        nullable=False,
        default="Software Developer"
    )

    experience_level = Column(
        String(50),
        nullable=False,
        default="Fresher"
    )

    difficulty = Column(
        String(50),
        nullable=False,
        default="Medium"
    )

    mode = Column(
        String(50),
        nullable=False,
        default="Text"
    )

    # ------------------------------------------------------
    # INTERVIEW INFORMATION
    # ------------------------------------------------------

    total_questions = Column(
        Integer,
        nullable=False,
        default=0
    )

    answered_questions = Column(
        Integer,
        nullable=False,
        default=0
    )

    # ------------------------------------------------------
    # AI SCORES
    # ------------------------------------------------------

    overall_score = Column(
        Integer,
        nullable=False,
        default=0
    )

    technical_score = Column(
        Integer,
        nullable=False,
        default=0
    )

    communication_score = Column(
        Integer,
        nullable=False,
        default=0
    )

    problem_solving_score = Column(
        Integer,
        nullable=False,
        default=0
    )

    confidence_score = Column(
        Integer,
        nullable=False,
        default=0
    )

    # ------------------------------------------------------
    # AI PERFORMANCE LABEL
    # ------------------------------------------------------

    performance_level = Column(
        String(50),
        nullable=False,
        default="Needs Improvement"
    )

    # ------------------------------------------------------
    # INTERVIEW STATUS
    # ------------------------------------------------------

    status = Column(
        String(50),
        nullable=False,
        default="completed"
    )

    # ------------------------------------------------------
    # OPTIONAL SUMMARY
    # ------------------------------------------------------

    summary = Column(
        Text,
        nullable=True
    )

    # ------------------------------------------------------
    # TIMESTAMP
    # ------------------------------------------------------

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )