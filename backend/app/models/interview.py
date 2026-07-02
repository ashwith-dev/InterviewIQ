import uuid
from typing import Optional
from sqlalchemy import (
    String, Integer, Float, Boolean, Text, DateTime,
    ForeignKey, CheckConstraint, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base


class Interview(Base):
    __tablename__ = "interviews"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid()
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    domain: Mapped[str] = mapped_column(String(50), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False)
    interview_type: Mapped[str] = mapped_column(String(20), nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="in_progress", nullable=False)
    overall_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    started_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="interviews")
    questions: Mapped[list["Question"]] = relationship(
        "Question", back_populates="interview", cascade="all, delete-orphan", lazy="selectin"
    )
    answers: Mapped[list["Answer"]] = relationship(
        "Answer", back_populates="interview", cascade="all, delete-orphan", lazy="selectin"
    )
    report: Mapped[Optional["Report"]] = relationship(
        "Report", back_populates="interview", uselist=False, cascade="all, delete-orphan", lazy="selectin"
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid()
    )
    interview_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_number: Mapped[int] = mapped_column(Integer, nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(20), nullable=False)
    is_followup: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    parent_question_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("questions.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    interview: Mapped["Interview"] = relationship("Interview", back_populates="questions")
    answer: Mapped[Optional["Answer"]] = relationship(
        "Answer", back_populates="question", uselist=False, cascade="all, delete-orphan", lazy="selectin"
    )
    followups: Mapped[list["Question"]] = relationship(
        "Question", foreign_keys=[parent_question_id], lazy="selectin"
    )


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid()
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    interview_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True
    )
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    time_taken_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    submitted_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    question: Mapped["Question"] = relationship("Question", back_populates="answer")
    interview: Mapped["Interview"] = relationship("Interview", back_populates="answers")
    evaluation: Mapped[Optional["Evaluation"]] = relationship(
        "Evaluation", back_populates="answer", uselist=False, cascade="all, delete-orphan", lazy="selectin"
    )


class Evaluation(Base):
    __tablename__ = "evaluations"
    __table_args__ = (
        CheckConstraint("technical_accuracy BETWEEN 0 AND 10", name="ck_eval_technical_accuracy"),
        CheckConstraint("communication BETWEEN 0 AND 10", name="ck_eval_communication"),
        CheckConstraint("problem_solving BETWEEN 0 AND 10", name="ck_eval_problem_solving"),
        CheckConstraint("completeness BETWEEN 0 AND 10", name="ck_eval_completeness"),
        CheckConstraint("practical_knowledge BETWEEN 0 AND 10", name="ck_eval_practical_knowledge"),
        CheckConstraint("overall_score BETWEEN 0 AND 10", name="ck_eval_overall_score"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid()
    )
    answer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("answers.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    technical_accuracy: Mapped[float] = mapped_column(Float, nullable=False)
    communication: Mapped[float] = mapped_column(Float, nullable=False)
    problem_solving: Mapped[float] = mapped_column(Float, nullable=False)
    completeness: Mapped[float] = mapped_column(Float, nullable=False)
    practical_knowledge: Mapped[float] = mapped_column(Float, nullable=False)
    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    ai_feedback: Mapped[str] = mapped_column(Text, nullable=False)
    evaluated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    answer: Mapped["Answer"] = relationship("Answer", back_populates="evaluation")


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid()
    )
    interview_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    hiring_recommendation: Mapped[str] = mapped_column(String(50), nullable=False)
    strengths: Mapped[dict] = mapped_column(JSONB, nullable=False)
    weaknesses: Mapped[dict] = mapped_column(JSONB, nullable=False)
    topics_to_study: Mapped[dict] = mapped_column(JSONB, nullable=False)
    learning_path: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    generated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    interview: Mapped["Interview"] = relationship("Interview", back_populates="report")
