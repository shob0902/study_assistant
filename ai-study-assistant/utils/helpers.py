# Framework-free helpers: errors, logging, state checks, prompt formatting and quiz grading.
import logging
import random
from typing import Any
class StudyAssistantError(Exception):
    pass
class MissingAPIKeyError(StudyAssistantError):
    pass
class LLMError(StudyAssistantError):
    pass
class QuizGenerationError(StudyAssistantError):
    pass
class InvalidStateError(StudyAssistantError):
    pass
_logger = logging.getLogger("study_assistant")
if not _logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("%(asctime)s %(message)s", "%H:%M:%S"))
    _logger.addHandler(_handler)
    _logger.setLevel(logging.INFO)
    _logger.propagate = False
# Log a tagged workflow message such as [NODE] Generating quiz.
def log_step(tag: str, message: str) -> None:
    _logger.info(f"[{tag}] {message}")
# Log an error message together with its traceback.
def log_error(message: str) -> None:
    _logger.exception(f"[ERROR] {message}")
# Raise InvalidStateError if any required state field is missing or empty.
def require_fields(state: dict[str, Any], fields: list[str], node_name: str) -> None:
    missing = [field for field in fields if not state.get(field)]
    if missing:
        raise InvalidStateError(
            f"The '{node_name}' step is missing data it needs: {', '.join(missing)}. "
            "Please start a new session."
        )
# Turn a list of strings into markdown bullet lines.
def bullet_list(items: list[str]) -> str:
    if not items:
        return "- (none)"
    return "\n".join(f"- {item}" for item in items)
# Convert an explanation dict into plain text for prompts.
def explanation_to_text(explanation: dict[str, Any]) -> str:
    return (
        f"Definition: {explanation.get('definition', '')}\n"
        f"Why it matters: {explanation.get('why_it_matters', '')}\n"
        f"How it works: {explanation.get('how_it_works', '')}\n"
        f"Analogy: {explanation.get('analogy', '')}\n"
        f"Key points:\n{bullet_list(explanation.get('key_points', []))}"
    )
# Return the newest re-explanation, or the original explanation if none exist.
def latest_explanation(state: dict[str, Any]) -> dict[str, Any]:
    re_explanations = state.get("re_explanations") or []
    return re_explanations[-1] if re_explanations else state.get("explanation", {})
# Describe graded quiz results as text for the evaluation prompt.
def results_to_text(results: list[dict[str, Any]]) -> str:
    lines = []
    for number, result in enumerate(results, start=1):
        status = "CORRECT" if result["is_correct"] else "WRONG"
        lines.append(
            f"Q{number} [{status}] {result['question']}\n"
            f"   Student answered: {result['user_answer']}\n"
            f"   Correct answer:   {result['correct_answer']}"
        )
    return "\n".join(lines)
_LETTERS = ["A", "B", "C", "D"]
# Find which option the LLM meant by its correct_answer value.
def _match_correct_answer(correct_answer: str, options: list[str]) -> str | None:
    answer = correct_answer.strip()
    for option in options:
        if option.lower() == answer.lower():
            return option
    letter = answer.rstrip(").:").upper()
    if letter in _LETTERS:
        return options[_LETTERS.index(letter)]
    if len(answer) > 3 and answer[0].upper() in _LETTERS and answer[1] in ").:":
        return _match_correct_answer(answer[2:], options)
    return None
# Keep only well-formed quiz questions and shuffle their options.
def clean_quiz_questions(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for question in questions:
        options = [str(option).strip() for option in question.get("options", [])]
        text = str(question.get("question", "")).strip()
        if not text or len(options) != 4 or len(set(options)) != 4:
            log_step("QUIZ", f"Skipping malformed question: {text[:60]!r}")
            continue
        correct = _match_correct_answer(str(question.get("correct_answer", "")), options)
        if correct is None:
            log_step("QUIZ", f"Skipping question with no matching answer: {text[:60]!r}")
            continue
        random.shuffle(options)
        cleaned.append(
            {
                "question": text,
                "options": options,
                "correct_answer": correct,
                "explanation": str(question.get("explanation", "")).strip(),
            }
        )
    return cleaned
# Grade the quiz and return per-question results, correct count and score.
def grade_quiz(
    quiz: list[dict[str, Any]], user_answers: list[str]
) -> tuple[list[dict[str, Any]], int, float]:
    results = []
    for question, user_answer in zip(quiz, user_answers):
        results.append(
            {
                "question": question["question"],
                "user_answer": user_answer,
                "correct_answer": question["correct_answer"],
                "is_correct": user_answer == question["correct_answer"],
                "explanation": question["explanation"],
            }
        )
    correct_count = sum(1 for result in results if result["is_correct"])
    score = correct_count / len(quiz) * 100 if quiz else 0.0
    return results, correct_count, score
