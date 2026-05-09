from pydantic import BaseModel, Field
from typing import List

class PromptHistory(BaseModel):
    prompt: str
    score: int

class PromptCopilotInput(BaseModel):
    model: str
    original_prompt: str
    previous_prompt: str | None = None
    current_prompt: str 
    original_score: int | None = None
    previous_score: int | None = None
    history: list[PromptHistory] = Field(default_factory=list)


class PromptCopilotResponse(BaseModel):
    predicted_goal: str
    prompt_quality_score: int
    score_reason: str
    improvement_from_original: int
    improvement_from_previous: int
    missing_areas: List[str]
    questions: List[str]
    suggestions: List[str]
    improved_prompt: str
    is_ready: bool