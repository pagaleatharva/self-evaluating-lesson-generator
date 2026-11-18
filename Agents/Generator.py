
from config import llm


def generate_lesson(topic: str, feedback: str = "") -> str:

    prompt = f"""
    You are an expert teacher.

    Create a complete beginner-friendly lesson.

    TOPIC: {topic}

    INSTRUCTIONS:

    1. Use simple English.
    2. Explain what the topic means.
    3. Explain why it is important.
    4. Explain how it works step by step.
    5. Include at least two examples.
    6. Explain difficult technical terms.
    7. Include a summary.

    Use these headings:

    # Introduction
    # What is it?
    # Why is it important?
    # How does it work?
    # Real-world examples
    # Important terms
    # Summary

    PREVIOUS EVALUATOR FEEDBACK:

    {feedback if feedback else "No previous feedback. This is the first generation."}

    If feedback is provided, carefully fix
    every reported problem.

    Generate the complete improved lesson.
    Do not only provide corrections.
    """

    response = llm.invoke(prompt)

    return response.content
