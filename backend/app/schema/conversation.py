from pydantic import BaseModel, Field

class ConversationDict(BaseModel):
    chat_id: str
    title: str
    model: str
    created_at: str
    updated_at: str

class ConversationResponse(BaseModel):
    chat_history: list[ConversationDict] | None = None
