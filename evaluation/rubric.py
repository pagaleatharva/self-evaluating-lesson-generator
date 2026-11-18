from typing import Literal

from pydantic import BaseModel, Field


class RubricCheck(BaseModel):
    status: Literal["PASS", "FAIL"] = Field(
        description="Must be either PASS or FAIL"
    )

    reason: str = Field(
        description="Explain why this check passed or failed"
    )

    improvement: str = Field(
        description="Explain how to fix the issue. Use an empty string if passed"
    )


class LessonEvaluation(BaseModel):
    accuracy: RubricCheck
    beginner_language: RubricCheck
    examples: RubricCheck
    jargon_explanation: RubricCheck
    key_coverage: RubricCheck
    teaching_flow: RubricCheck