# Streamlit UI that starts, pauses and resumes the LangGraph study workflow.
import uuid
from typing import Any
import streamlit as st
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command
from graph.state import MAX_RETRIES, PASSING_SCORE, create_initial_state
from graph.workflow import (
    NODE_LABELS,
    TEXT_DIAGRAM,
    WAIT_FOR_ANSWERS,
    build_workflow,
    get_mermaid_diagram,
)
from llm.model import MODEL, NODE_API_KEYS, missing_api_keys
from ui import cards
from ui.theme import inject_styles
from ui.three_scenes import END_NODE, embed, hero_scene, rocket_scene, score_scene, thinking_scene, workflow_scene
from utils.helpers import StudyAssistantError, log_error, log_step
MAX_TOPIC_LENGTH = 300
SUGGESTED_TOPICS = ["What is an embedding?", "How does photosynthesis work?", "What is recursion?"]
st.set_page_config(page_title="AI Study Assistant", layout="centered")
# Build the compiled graph once per server process.
@st.cache_resource
def get_graph() -> CompiledStateGraph:
    return build_workflow()
# Create the st.session_state keys on the first run.
def init_session_state() -> None:
    defaults: dict[str, Any] = {
        "thread_id": None,
        "study_state": None,
        "next_nodes": (),
        "execution_log": [],
        "error": None,
        "graph_png": None,
        "celebrated": set(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
# Return the LangGraph config holding this session's thread_id.
def graph_config() -> dict[str, Any]:
    return {"configurable": {"thread_id": st.session_state.thread_id}}
# Copy the checkpointed graph state into st.session_state.
def sync_state_from_graph() -> None:
    snapshot = get_graph().get_state(graph_config())
    st.session_state.study_state = dict(snapshot.values)
    st.session_state.next_nodes = tuple(snapshot.next)
# Run or resume the graph with a 3D thinking animation and live progress, then rerun the page.
def run_graph(graph_input: Any) -> None:
    st.session_state.error = None
    embed(thinking_scene(), 170)
    with st.status("LangGraph is working...", expanded=True) as status:
        try:
            for update in get_graph().stream(graph_input, graph_config(), stream_mode="updates"):
                for node_name in update:
                    if node_name == "__interrupt__":
                        st.write("Paused — waiting for your quiz answers")
                        st.session_state.execution_log.append("interrupt (waiting for user)")
                    else:
                        st.write(NODE_LABELS.get(node_name, node_name))
                        st.session_state.execution_log.append(node_name)
            status.update(label="Done!", state="complete", expanded=False)
        except StudyAssistantError as error:
            log_error("Graph stopped with a known error")
            st.session_state.error = str(error)
            status.update(label="Something went wrong", state="error")
        except Exception:
            log_error("Graph stopped with an unexpected error")
            st.session_state.error = (
                "An unexpected error occurred. Check the terminal for details, then try again."
            )
            status.update(label="Something went wrong", state="error")
    sync_state_from_graph()
    st.rerun()
# Start a new study session for a topic.
def start_session(topic: str) -> None:
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.execution_log = []
    log_step("UI", f"New study session for: {topic!r}")
    log_step("GRAPH", "Starting workflow")
    run_graph(create_initial_state(topic))
# Resume the paused graph with the student's quiz answers.
def submit_answers(answers: list[str]) -> None:
    log_step("GRAPH", "Resuming workflow with the student's answers")
    run_graph(Command(resume=answers))
# Clear the current study session from st.session_state.
def reset_session() -> None:
    for key in ["thread_id", "study_state", "next_nodes", "execution_log", "error"]:
        del st.session_state[key]
    init_session_state()
# Return where the workflow is: idle, quiz, finished or stopped.
def session_status() -> str:
    state = st.session_state.study_state
    next_nodes = st.session_state.next_nodes
    if not state:
        return "idle"
    if WAIT_FOR_ANSWERS in next_nodes:
        return "quiz"
    if next_nodes:
        return "stopped"
    if state.get("recommendation"):
        return "finished"
    return "stopped"
# Work out which study stages are done, active or still to come for the progress stepper.
def study_steps(state: dict[str, Any], status: str) -> list[tuple[str, str, str]]:
    stages = [
        ("1", "Understand", bool(state.get("topic_analysis"))),
        ("2", "Learn", bool(state.get("explanation"))),
        ("3", "Examples", bool(state.get("examples"))),
        ("4", "Quiz", bool(state.get("attempts")) and status != "quiz"),
        ("5", "Results", bool(state.get("attempts")) and status != "quiz"),
        ("6", "Next", bool(state.get("recommendation"))),
    ]
    active = next((index for index, (_, _, done) in enumerate(stages) if not done), None)
    return [
        (icon, label, "done" if done else ("active" if index == active else ""))
        for index, (icon, label, done) in enumerate(stages)
    ]
# Return the workflow node to highlight as current in the 3D map.
def current_workflow_node() -> str | None:
    status = session_status()
    if status == "quiz":
        return WAIT_FOR_ANSWERS
    if status == "finished":
        return END_NODE
    if status == "stopped" and st.session_state.next_nodes:
        return st.session_state.next_nodes[0]
    return None
# Draw the sidebar with settings, API key mapping and session details.
def render_sidebar() -> None:
    with st.sidebar:
        st.html(cards.sidebar_header(MODEL, PASSING_SCORE, MAX_RETRIES))
        with st.expander("API key per node"):
            st.code("\n".join(f"{node:<22} {key}" for node, key in NODE_API_KEYS.items()))
            st.caption("wait_for_answers doesn't call Groq, so it needs no key.")
        state = st.session_state.study_state
        if not state:
            return
        st.subheader("Current session")
        title = state.get("topic_analysis", {}).get("clean_topic") or state.get("topic", "")
        rows = [
            ("Topic", title),
            ("Quiz attempts", str(len(state.get("attempts", [])))),
            ("Retries used", f"{state.get('retry_count', 0)}/{MAX_RETRIES}"),
            ("Status", session_status()),
        ]
        if state.get("attempts"):
            rows.insert(3, ("Latest score", f"{state.get('score', 0):.0f}%"))
        st.html(cards.sidebar_session(rows))
        with st.expander("Graph execution log"):
            st.code("\n".join(f"→ {step}" for step in st.session_state.execution_log) or "(empty)")
        with st.expander("Raw graph state"):
            st.json(state_for_display(state), expanded=False)
        if st.button("Reset session", width="stretch"):
            reset_session()
            st.rerun()
# Copy the state with correct answers hidden while a quiz is open.
def state_for_display(state: dict[str, Any]) -> dict[str, Any]:
    display = dict(state)
    if session_status() == "quiz":
        display["quiz"] = [
            {"question": q["question"], "options": q["options"], "correct_answer": "hidden"}
            for q in state.get("quiz", [])
        ]
    return display
# Draw the hero: animated title on the left and the 3D knowledge crystal on the right.
def render_hero() -> None:
    text_col, scene_col = st.columns([3, 2], vertical_alignment="center")
    with text_col:
        st.html(cards.hero_intro())
    with scene_col:
        embed(hero_scene(), 250)
# Draw the explanation tiles, marked as simpler for re-explanations.
def render_explanation(explanation: dict[str, Any], simpler: bool = False) -> None:
    st.html(cards.explanation_cards(explanation, simpler))
# Draw the examples as 3D flip cards.
def render_examples(examples: list[dict[str, Any]]) -> None:
    st.header("Examples")
    st.html(cards.example_cards(examples))
# Draw the quiz form with animated question cards and submit the answers when complete.
def render_quiz_form(state: dict[str, Any]) -> None:
    quiz = state["quiz"]
    attempt_number = len(state.get("attempts", [])) + 1
    st.header("Quiz" if attempt_number == 1 else f"Quiz — Attempt {attempt_number}")
    st.html(cards.quiz_intro(len(quiz), PASSING_SCORE, attempt_number > 1))
    form_id = f"{st.session_state.thread_id}_{attempt_number}"
    with st.form(f"quiz_form_{form_id}"):
        answers = []
        for index, question in enumerate(quiz):
            with st.container(key=f"qcard_{form_id}_{index}"):
                answer = st.radio(
                    f"**Q{index + 1}. {question['question']}**",
                    options=question["options"],
                    index=None,
                    key=f"answer_{form_id}_{index}",
                )
            answers.append(answer)
        submitted = st.form_submit_button("Submit Quiz", type="primary", width="stretch")
    if submitted:
        if any(answer is None for answer in answers):
            st.warning("Please answer every question before submitting.")
        else:
            submit_answers(answers)
# Draw one attempt: 3D score scene for the latest attempt, summary cards and per-question results.
def render_attempt_result(attempt: dict[str, Any], is_latest: bool) -> None:
    number = attempt["attempt_number"]
    st.header(f"Quiz Results — Attempt {number}")
    if is_latest:
        embed(score_scene(attempt["score"], attempt["passed"]), 240)
        celebration_key = f"{st.session_state.thread_id}_{number}"
        if attempt["passed"] and celebration_key not in st.session_state.celebrated:
            st.session_state.celebrated.add(celebration_key)
            st.balloons()
    st.html(cards.result_summary(attempt, MAX_RETRIES))
    with st.expander("See every question with explanations", expanded=is_latest):
        st.html(cards.question_results(attempt["results"]))
# Draw the next-topic recommendation with the 3D rocket and its start button.
def render_recommendation(state: dict[str, Any]) -> None:
    recommendation = state["recommendation"]
    passed = state.get("score", 0) >= PASSING_SCORE
    st.header("What's Next?")
    scene_col, card_col = st.columns([2, 3], vertical_alignment="center")
    with scene_col:
        embed(rocket_scene(), 260)
    with card_col:
        st.html(cards.recommendation_card(recommendation, passed))
    if st.button(f"Start learning: {recommendation['next_topic']}", type="primary", width="stretch"):
        start_session(recommendation["next_topic"])
# Draw the whole study session from the saved state.
def render_session() -> None:
    state = st.session_state.study_state
    status = session_status()
    st.html(cards.stepper(study_steps(state, status)))
    analysis = state.get("topic_analysis")
    if analysis:
        st.html(cards.topic_card(analysis))
    if state.get("explanation"):
        st.header("Explanation")
        render_explanation(state["explanation"])
    if state.get("examples"):
        render_examples(state["examples"])
    attempts = state.get("attempts", [])
    re_explanations = state.get("re_explanations", [])
    for index, attempt in enumerate(attempts):
        render_attempt_result(attempt, is_latest=index == len(attempts) - 1)
        if index < len(re_explanations):
            st.header("Let's Try a Simpler Explanation")
            render_explanation(re_explanations[index], simpler=True)
    if status == "quiz":
        render_quiz_form(state)
    elif status == "finished":
        render_recommendation(state)
    elif status == "stopped":
        next_nodes = st.session_state.next_nodes
        if next_nodes:
            st.warning(f"The workflow stopped before finishing. Next step: `{next_nodes[0]}`")
            if st.button("Retry this step", type="primary"):
                log_step("GRAPH", f"Retrying from checkpoint at '{next_nodes[0]}'")
                run_graph(None)
        else:
            st.error("The study session is in an unexpected state. Please reset the session.")
# Draw the workflow as an interactive 3D map, text, Mermaid source and an optional image.
def render_graph_section() -> None:
    with st.expander("View LangGraph Workflow"):
        map_tab, text_tab, mermaid_tab = st.tabs(["3D map", "Text", "Mermaid"])
        with map_tab:
            visited = {step for step in st.session_state.execution_log if step in NODE_LABELS}
            embed(workflow_scene(visited, current_workflow_node()), 400)
            st.caption("Green nodes already ran in this session, the glowing amber node is where the graph is now.")
        with text_tab:
            st.code(TEXT_DIAGRAM, language=None)
        with mermaid_tab:
            graph = get_graph()
            st.markdown("Generated by `graph.get_graph().draw_mermaid()`")
            st.code(get_mermaid_diagram(graph), language=None)
            st.caption("Tip: paste this into https://mermaid.live to see it drawn.")
            if st.button("Render graph image"):
                try:
                    st.session_state.graph_png = graph.get_graph().draw_mermaid_png()
                except Exception:
                    log_error("Could not render graph image")
                    st.warning(
                        "Could not render the image (it needs internet access to mermaid.ink). "
                        "The 3D map and Mermaid source show the same graph."
                    )
            if st.session_state.graph_png:
                st.image(st.session_state.graph_png)
# Build the page: styles, sidebar, hero, API key check, topic form, session and graph view.
def main() -> None:
    init_session_state()
    inject_styles()
    render_sidebar()
    render_hero()
    missing_keys = missing_api_keys()
    if missing_keys:
        st.error(
            f"**Missing Groq API keys:** {', '.join(missing_keys)}  \n"
            "Copy `.env.example` to `.env`, paste your Groq API keys, then restart the app."
        )
        render_graph_section()
        st.stop()
    with st.form("topic_form"):
        topic = st.text_input("What do you want to learn?", placeholder="What is an embedding?")
        start_clicked = st.form_submit_button("Start Learning", type="primary", width="stretch")
    if start_clicked:
        if not topic.strip():
            st.warning("Please enter a topic first.")
        elif len(topic) > MAX_TOPIC_LENGTH:
            st.warning(f"Please keep the topic under {MAX_TOPIC_LENGTH} characters.")
        else:
            start_session(topic.strip())
    if not st.session_state.study_state:
        st.caption("Need an idea? Try one of these:")
        for column, suggestion in zip(st.columns(len(SUGGESTED_TOPICS)), SUGGESTED_TOPICS):
            if column.button(suggestion, key=f"suggest_{suggestion}", width="stretch"):
                start_session(suggestion)
    if st.session_state.error:
        st.error(st.session_state.error)
    if st.session_state.study_state:
        render_session()
    st.divider()
    render_graph_section()
main()
