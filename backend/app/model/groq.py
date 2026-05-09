from langchain_groq import ChatGroq
from app.config import settings

def get_groq_model(model_name: str, temperature: float = 0.2, max_tokens: int = 2048) -> ChatGroq:
    return ChatGroq(
        model=settings.AVAILABLE_MODELS["groq"][model_name],
        groq_api_key=settings.GROQ_API_KEY,
        temperature=temperature,
        max_tokens=max_tokens,
    )