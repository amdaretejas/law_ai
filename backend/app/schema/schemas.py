from pydantic import BaseModel, Field, field_validator

class MessageDict(BaseModel):
    role: str
    content: str

class ChatInput(BaseModel):
    prompt: str
    model: str = Field(..., min_length=1)
    chat_id: str | None = Field(default=None)
    history: list[MessageDict] = Field(default_factory=list)

    @field_validator("prompt")
    @classmethod
    def prompt_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Prompt cannot be blank")
        return v.strip()

class ChatSummary(BaseModel):
    chat_id: str
    title: str
    model: str
    created_at: str
    updated_at: str
 
class ChatHistoryResponse(BaseModel):
    chat_id: str | None = None
    chat_history: list[dict] 