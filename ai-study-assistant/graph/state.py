# Shared StudyState passed between graph nodes, plus workflow settings.
import operator
from typing import Annotated, Any, TypedDict
PASSING_SCORE = 70
MAX_RETRIES = 2
FIRST_QUIZ_SIZE = 5
RETRY_QUIZ_SIZE = 3
class StudyState(TypedDict):
    topic: str
    topic_analysis: dict[str, Any]
    explanation: dict[str, Any]
    examples: list[dict[str, Any]]
    quiz: list[dict[str, Any]]
    user_answers: list[str]
    score: float
    feedback: str
    weak_concepts: list[str]
    attempts: Annotated[list[dict[str, Any]], operator.add]
    re_explanations: Annotated[list[dict[str, Any]], operator.add]
    retry_count: int
    recommendation: dict[str, Any]
    next_topic: str
# Build the starting StudyState for a new topic.
def create_initial_state(topic: str) -> StudyState:
    return StudyState(
        topic=topic.strip(),
        topic_analysis={},
        explanation={},
        examples=[],
        quiz=[],
        user_answers=[],
        score=0.0,
        feedback="",
        weak_concepts=[],
        attempts=[],
        re_explanations=[],
        retry_count=0,
        recommendation={},
        next_topic="",
    )
