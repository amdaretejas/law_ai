from pydantic import BaseModel, Field

class MessageDict(BaseModel):
    role: str
    content: str
    qna_id: str

class ChatInput(BaseModel):
    prompt: str 
    model: str
    chat_id: str | None = None

class ChatResponse(BaseModel):
    response: str
    chat_id: str | None = None
    history: list[MessageDict] | None = None

class MessagesResponse(BaseModel):
    chat_id: str
    messages: list[MessageDict]