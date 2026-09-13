# Routing function for the conditional edge that runs after quiz evaluation.
from typing import Literal
from graph.state import MAX_RETRIES, PASSING_SCORE, StudyState
from utils.helpers import log_step
RE_EXPLAIN = "re_explain"
RECOMMEND = "recommend"
# Router: choose re_explain or recommend from the score and retry count.
def route_after_evaluation(state: StudyState) -> Literal["re_explain", "recommend"]:
    score = state.get("score", 0.0)
    retry_count = state.get("retry_count", 0)
    log_step("ROUTER", f"Score = {score:.0f}, retries used = {retry_count}/{MAX_RETRIES}")
    if score >= PASSING_SCORE:
        log_step("ROUTER", f"Passed -> going to {RECOMMEND}")
        return RECOMMEND
    if retry_count >= MAX_RETRIES:
        log_step("ROUTER", f"Max retries reached -> going to {RECOMMEND} with extra guidance")
        return RECOMMEND
    log_step("ROUTER", f"Below {PASSING_SCORE}% -> going to {RE_EXPLAIN}")
    return RE_EXPLAIN
