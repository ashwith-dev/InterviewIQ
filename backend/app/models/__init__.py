# This file imports all models so Alembic can discover them
# and auto-generate migrations correctly.
from app.models.user import User
from app.models.interview import Interview, Question, Answer, Evaluation, Report

__all__ = ["User", "Interview", "Question", "Answer", "Evaluation", "Report"]
