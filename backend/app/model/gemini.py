from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

def get_gemini_model(model_name: str, temprature: float = 0.2, max_output_tokens: int = 2048) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=settings.AVAILABLE_MODELS["google"][model_name],
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=temprature,
        max_output_tokens=max_output_tokens,
    )
