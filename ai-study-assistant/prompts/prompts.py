# LangChain ChatPromptTemplates, one small prompt per study task.
from langchain_core.prompts import ChatPromptTemplate
TUTOR_SYSTEM = (
    "You are a patient, friendly tutor who explains things to complete beginners. "
    "Use simple words, short sentences and concrete everyday examples. "
    "Avoid jargon; if you must use a technical term, explain it immediately."
)
TOPIC_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", TUTOR_SYSTEM),
        (
            "human",
            "A student wants to learn about the following:\n\n"
            "\"{topic}\"\n\n"
            "Analyse this request. Give the topic a clean short title, identify its "
            "subject area, estimate its difficulty, list the key concepts a beginner "
            "must understand, and list any helpful prerequisites.",
        ),
    ]
)
EXPLANATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", TUTOR_SYSTEM),
        (
            "human",
            "Explain the topic \"{topic}\" to a beginner.\n\n"
            "Make sure the explanation covers these key concepts:\n{key_concepts}\n\n"
            "Include a clear definition, why it matters, how it works step by step, "
            "and a simple everyday analogy.",
        ),
    ]
)
EXAMPLES_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", TUTOR_SYSTEM),
        (
            "human",
            "The student just read this explanation of \"{topic}\":\n\n"
            "{explanation}\n\n"
            "Give 3 concrete, varied, real-world examples that make the topic easy "
            "to picture. Keep each example short.",
        ),
    ]
)
QUIZ_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You write clear multiple-choice quizzes that check real understanding, "
            "not memorisation of exact wording.",
        ),
        (
            "human",
            "Create exactly {num_questions} multiple-choice questions about \"{topic}\" "
            "based on this explanation:\n\n{explanation}\n\n"
            "Focus: {focus}\n\n"
            "Do not repeat these earlier questions:\n{avoid_questions}\n\n"
            "Rules:\n"
            "- Each question has exactly 4 options.\n"
            "- Exactly one option is correct.\n"
            "- Do not prefix options with letters or numbers.\n"
            "- correct_answer must be copied exactly from the options.\n"
            "- Wrong options should be plausible, not silly.\n"
            "- Suitable for a beginner who read the explanation.",
        ),
    ]
)
EVALUATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", TUTOR_SYSTEM),
        (
            "human",
            "A student took a quiz about \"{topic}\" and scored {score}%.\n\n"
            "Here are their results:\n{results}\n\n"
            "Look at the mistakes and identify which underlying concepts the student "
            "is struggling with (not just which questions were wrong). Also note what "
            "they clearly understand. Be encouraging and specific.",
        ),
    ]
)
RE_EXPLANATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", TUTOR_SYSTEM),
        (
            "human",
            "A student did not pass a quiz about \"{topic}\" (re-explanation #{attempt}).\n\n"
            "This is the explanation they already read:\n{previous_explanation}\n\n"
            "They are struggling with:\n{weak_concepts}\n\n"
            "Explain the topic again in a SIMPLER and DIFFERENT way. Focus especially "
            "on the concepts they struggle with. Use a new analogy, shorter sentences, "
            "and no jargon at all.",
        ),
    ]
)
RECOMMENDATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", TUTOR_SYSTEM),
        (
            "human",
            "A student has finished studying \"{topic}\".\n"
            "Final quiz score: {score}%\n"
            "Passed: {passed}\n\n"
            "Strengths:\n{strengths}\n\n"
            "Weak concepts:\n{weak_concepts}\n\n"
            "Known prerequisites for this topic:\n{prerequisites}\n\n"
            "If the student PASSED: recommend a natural next topic that builds on "
            "this one, and explain why.\n"
            "If the student did NOT pass after several attempts: be kind, recommend a "
            "simpler foundational topic that will help them come back to this one, "
            "and give practical extra guidance for studying.",
        ),
    ]
)
if __name__ == "__main__":
    messages = EXPLANATION_PROMPT.invoke(
        {"topic": "Embeddings", "key_concepts": "- vectors\n- similarity"}
    ).to_messages()
    for message in messages:
        print(f"--- {message.type.upper()} ---\n{message.content}\n")
