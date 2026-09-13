# Pydantic models describing the structured output expected from the LLM.
from pydantic import BaseModel, Field
class TopicAnalysis(BaseModel):
    """A short analysis of what the student wants to learn."""
    clean_topic: str = Field(
        description="The topic rewritten as a short, clear title, e.g. 'Embeddings'."
    )
    subject_area: str = Field(
        description="The broader field this topic belongs to, e.g. 'Machine Learning'."
    )
    difficulty: str = Field(
        description="One of: beginner, intermediate, advanced."
    )
    key_concepts: list[str] = Field(
        description="3 to 5 core concepts a beginner must understand for this topic."
    )
    prerequisites: list[str] = Field(
        description="0 to 3 topics that are helpful to know before this one."
    )
class Explanation(BaseModel):
    """A beginner-friendly explanation of a topic."""
    definition: str = Field(
        description="A simple 1-3 sentence definition with no unexplained jargon."
    )
    why_it_matters: str = Field(
        description="Why this topic is useful or important in the real world."
    )
    how_it_works: str = Field(
        description="A step-by-step, plain-language description of how it works."
    )
    analogy: str = Field(
        description="A simple everyday analogy that makes the idea intuitive."
    )
    key_points: list[str] = Field(
        description="3 to 5 short bullet points summarising the most important ideas."
    )
class Example(BaseModel):
    """One concrete example of the topic."""
    title: str = Field(description="A short title for the example.")
    description: str = Field(
        description="2-4 sentences describing the example and how it shows the topic."
    )
class ExampleSet(BaseModel):
    """A list of concrete examples."""
    examples: list[Example] = Field(description="Between 2 and 4 examples.")
class QuizQuestion(BaseModel):
    """One multiple-choice quiz question."""
    question: str = Field(description="The question text.")
    options: list[str] = Field(
        description="Exactly 4 answer options. Do NOT prefix them with A), B), 1., etc."
    )
    correct_answer: str = Field(
        description="The correct option, copied EXACTLY from the options list."
    )
    explanation: str = Field(
        description="1-2 sentences explaining why the correct answer is right."
    )
class Quiz(BaseModel):
    """A multiple-choice quiz."""
    questions: list[QuizQuestion] = Field(description="The quiz questions.")
class Evaluation(BaseModel):
    """Personalised feedback on a student's quiz attempt."""
    overall_feedback: str = Field(
        description="2-3 encouraging sentences about how the student did."
    )
    strengths: list[str] = Field(
        description="Concepts the student clearly understands (can be empty)."
    )
    weak_concepts: list[str] = Field(
        description="Specific concepts the student is struggling with (can be empty)."
    )
    study_tip: str = Field(description="One practical tip for what to do next.")
class Recommendation(BaseModel):
    """A recommendation for what the student should learn next."""
    summary: str = Field(
        description="1-2 sentences summarising the student's understanding of the topic."
    )
    next_topic: str = Field(description="The recommended next topic, as a short title.")
    reason: str = Field(description="Why this topic is a good next step.")
    extra_guidance: list[str] = Field(
        description=(
            "Additional study guidance. Give 2-4 items if the student did not pass, "
            "otherwise it can be empty."
        )
    )
