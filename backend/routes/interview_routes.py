from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Interview
from backend.services.ai_evaluator import ai_evaluator


router = APIRouter(
    prefix="/api/interview",
    tags=["Interview"]
)


# ==========================================================
# REQUEST MODELS
# ==========================================================

class EvaluateAnswerRequest(BaseModel):
    question: str
    answer: str
    interview_type: Optional[str] = "Technical"
    role: Optional[str] = "Software Developer"


class SaveInterviewRequest(BaseModel):
    user_id: int

    interview_type: str = "Technical"
    role: str = "Software Developer"
    experience_level: str = "Fresher"
    difficulty: str = "Medium"
    mode: str = "Text"

    total_questions: int = 0
    answered_questions: int = 0

    overall_score: int = Field(default=0, ge=0, le=100)
    technical_score: int = Field(default=0, ge=0, le=100)
    communication_score: int = Field(default=0, ge=0, le=100)
    problem_solving_score: int = Field(default=0, ge=0, le=100)
    confidence_score: int = Field(default=0, ge=0, le=100)

    performance_level: str = "Needs Improvement"

    summary: Optional[str] = None


# ==========================================================
# HEALTH
# ==========================================================

@router.get("/health")
def interview_health():

    return {
        "status": "online",
        "service": "Interview Engine",
        "ai_evaluator": "ready"
    }


# ==========================================================
# AI EVALUATION
# ==========================================================

@router.post("/evaluate")
def evaluate_answer(
    request: EvaluateAnswerRequest
):

    question = request.question.strip()
    answer = request.answer.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    if not answer:
        raise HTTPException(
            status_code=400,
            detail="Answer cannot be empty."
        )

    if len(answer) < 3:
        raise HTTPException(
            status_code=400,
            detail="Please provide a more complete answer."
        )

    try:

        result = ai_evaluator.evaluate(
            question=question,
            answer=answer,
            interview_type=request.interview_type,
            role=request.role
        )

        return {
            "status": "success",
            "message": "Answer evaluated successfully.",
            "result": result
        }

    except Exception as error:

        print("AI EVALUATION ERROR:", error)

        raise HTTPException(
            status_code=500,
            detail="AI evaluation failed."
        )


# ==========================================================
# SAVE COMPLETED INTERVIEW
# ==========================================================

@router.post("/save")
def save_interview(
    request: SaveInterviewRequest,
    db: Session = Depends(get_db)
):

    interview = Interview(
        user_id=request.user_id,

        interview_type=request.interview_type,
        role=request.role,
        experience_level=request.experience_level,
        difficulty=request.difficulty,
        mode=request.mode,

        total_questions=request.total_questions,
        answered_questions=request.answered_questions,

        overall_score=request.overall_score,
        technical_score=request.technical_score,
        communication_score=request.communication_score,
        problem_solving_score=request.problem_solving_score,
        confidence_score=request.confidence_score,

        performance_level=request.performance_level,

        status="completed",

        summary=request.summary
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)

    return {
        "status": "success",
        "message": "Interview result saved successfully.",
        "interview": {
            "id": interview.id,
            "user_id": interview.user_id,
            "overall_score": interview.overall_score,
            "technical_score": interview.technical_score,
            "communication_score": interview.communication_score,
            "problem_solving_score": interview.problem_solving_score,
            "confidence_score": interview.confidence_score,
            "performance_level": interview.performance_level,
            "created_at": interview.created_at
        }
    }


# ==========================================================
# INTERVIEW HISTORY
# ==========================================================

@router.get("/history/{user_id}")
def interview_history(
    user_id: int,
    db: Session = Depends(get_db)
):

    interviews = (
        db.query(Interview)
        .filter(Interview.user_id == user_id)
        .order_by(Interview.created_at.desc())
        .all()
    )

    return {
        "status": "success",
        "count": len(interviews),
        "interviews": [
            {
                "id": interview.id,
                "interview_type": interview.interview_type,
                "role": interview.role,
                "experience_level": interview.experience_level,
                "difficulty": interview.difficulty,
                "mode": interview.mode,
                "total_questions": interview.total_questions,
                "answered_questions": interview.answered_questions,
                "overall_score": interview.overall_score,
                "technical_score": interview.technical_score,
                "communication_score": interview.communication_score,
                "problem_solving_score": interview.problem_solving_score,
                "confidence_score": interview.confidence_score,
                "performance_level": interview.performance_level,
                "status": interview.status,
                "summary": interview.summary,
                "created_at": interview.created_at
            }
            for interview in interviews
        ]
    }


# ==========================================================
# LATEST INTERVIEW
# ==========================================================

@router.get("/latest/{user_id}")
def latest_interview(
    user_id: int,
    db: Session = Depends(get_db)
):

    interview = (
        db.query(Interview)
        .filter(Interview.user_id == user_id)
        .order_by(Interview.created_at.desc())
        .first()
    )

    if not interview:

        return {
            "status": "success",
            "found": False,
            "message": "No completed interviews found."
        }

    return {
        "status": "success",
        "found": True,
        "interview": {
            "id": interview.id,
            "overall_score": interview.overall_score,
            "technical_score": interview.technical_score,
            "communication_score": interview.communication_score,
            "problem_solving_score": interview.problem_solving_score,
            "confidence_score": interview.confidence_score,
            "performance_level": interview.performance_level,
            "role": interview.role,
            "interview_type": interview.interview_type,
            "created_at": interview.created_at
        }
    }