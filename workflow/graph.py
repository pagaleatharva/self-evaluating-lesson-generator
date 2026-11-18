
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from Agents.Generator import generate_lesson
from Agents.evaluation import evaluate_lesson
from memory.database import (
    initialize_database,
    save_lesson_run,
    get_learning_memory
)

# 1. Define workflow state
class LessonState(TypedDict):

    topic: str
    lesson: str
    feedback: str
    evaluation: dict
    retry_count: int
    rejection_log: list
    status: str


# 2. Generator node
def generator_node(state: LessonState):

    print("\n--- GENERATOR AGENT RUNNING ---")

    lesson = generate_lesson(
        topic=state["topic"],
        feedback=state.get("feedback", "")
    )

    return {
        "lesson": lesson
    }


# 3. Evaluator node
def evaluator_node(state: LessonState):

    print("\n--- EVALUATOR AGENT RUNNING ---")

    result = evaluate_lesson(
        state["topic"],
        state["lesson"]
    )

    evaluation = result.model_dump()

    checks = list(evaluation.values())

    passed = all(
        check["status"] == "PASS"
        for check in checks
    )

    # Prepare feedback for the generator
    failed_checks = [
        f"{name}: {check['reason']}. "
        f"Suggested fix: {check['improvement']}"
        for name, check in evaluation.items()
        if check["status"] == "FAIL"
    ]

    rejection_log = list(state.get("rejection_log", []))

    if not passed:

        rejection_log.append({
            "attempt": state["retry_count"] + 1,
            "failed_checks": failed_checks
        })

    return {
        "evaluation": evaluation,
        "feedback": "\n".join(failed_checks),
        "rejection_log": rejection_log,
        "status": "PASS" if passed else "FAIL"
    }


# 4. Decision function
def decide_next_step(state: LessonState):

    if state["status"] == "PASS":
        print("\nLesson approved!")
        return "approved"

    if state["retry_count"] < 2:
        print("\nLesson rejected. Regenerating...")
        return "retry"

    print("\nMaximum retries reached.")
    return "rejected"


# 5. Increase retry counter
def prepare_retry(state: LessonState):

    return {
        "retry_count": state["retry_count"] + 1
    }


# 6. Build LangGraph workflow
builder = StateGraph(LessonState)

builder.add_node("generator", generator_node)
builder.add_node("evaluator", evaluator_node)
builder.add_node("prepare_retry", prepare_retry)

builder.add_edge(START, "generator")

builder.add_edge("generator", "evaluator")

builder.add_conditional_edges(
    "evaluator",
    decide_next_step,
    {
        "approved": END,
        "retry": "prepare_retry",
        "rejected": END
    }
)

builder.add_edge("prepare_retry", "generator")


# 7. Compile workflow
lesson_workflow = builder.compile()


# 8. Function to execute workflow

def run_workflow(topic: str):

    # Initialize database
    initialize_database()

    # Retrieve previous failures
    previous_failures = get_learning_memory(topic)

    # Convert previous failures into prompt feedback
    memory_feedback = ""

    if previous_failures:

        memory_feedback = (
            "LEARN FROM PREVIOUS RUNS:\n"
            + "\n".join(
                f"- {failure}"
                for failure in previous_failures
            )
        )

    # Initial workflow state
    initial_state = {
        "topic": topic,
        "lesson": "",
        "feedback": memory_feedback,
        "evaluation": {},
        "retry_count": 0,
        "rejection_log": [],
        "status": "RUNNING"
    }

    # Execute LangGraph workflow
    result = lesson_workflow.invoke(initial_state)

    # Save current run into SQLite
    save_lesson_run(result)

    return result
