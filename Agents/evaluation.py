
from config import llm
from evaluation.rubric import LessonEvaluation


# Convert the Groq model into a structured-output model
evaluator_llm = llm.with_structured_output(
    LessonEvaluation
)


def evaluate_lesson(topic: str, lesson: str):

    prompt = f"""
    You are a strict educational quality evaluator.

    Your job is to evaluate a beginner lesson.

    TOPIC:
    {topic}

    GENERATED LESSON:
    {lesson}

    Evaluate the lesson using these six criteria.

    1. ACCURACY:
    Is the information factually correct?
    Flag incorrect or misleading explanations.

    2. BEGINNER LANGUAGE:
    Can a student with no technical background
    understand the lesson?

    3. EXAMPLES:
    Does the lesson contain at least two
    useful and understandable examples?

    4. JARGON EXPLANATION:
    Are technical and difficult words
    explained in simple English?

    5. KEY COVERAGE:
    Does the lesson explain what the topic is,
    why it matters, and how it works?

    6. TEACHING FLOW:
    Is the lesson organised logically
    from basic concepts to examples?

    STRICT RULES:

    - Each criterion must be PASS or FAIL.
    - Do not give partial marks.
    - Do not pass a criterion just because
      the lesson looks professionally written.
    - Give a clear reason for every decision.
    - If a criterion fails, suggest a specific fix.
    - If a criterion passes, improvement must be empty.
    - Be strict and honest.

    Return the results in the required
    structured format.
    """

    result = evaluator_llm.invoke(prompt)

    return result
