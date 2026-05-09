from pydantic_settings import BaseSettings
from typing import ClassVar
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):

    APP_ENV: str = os.getenv("APP_ENV")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")

    MONGODB_URL: str = os.getenv("MONGODB_URL")
    DB_NAME: str = os.getenv("DB_NAME")

    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI")
    FRONTEND_URL: str =  os.getenv("FRONTEND_URL")

    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_TRACING_V2: str = os.getenv("LANGCHAIN_TRACING_V2")
    LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT")

    FREE_DAILY_LIMIT: int = os.getenv("FREE_DAILY_LIMIT")
    PRO_DAILY_LIMIT: int = os.getenv("PRO_DAILY_LIMIT")


    AVAILABLE_MODELS: ClassVar[dict] = {
        "google": {
            "gemini_2_5_flash": "gemini-2.5-flash",
            "gemini_2_5_pro": "gemini-2.5-pro",
            "gemini_embedding_1": "models/gemini-embedding-001",
            "gemini_embedding_2": "models/gemini-embedding-004",
        },
        "groq": {
            "llama_3_1_8b_instant": "llama-3.1-8b-instant",
            "llama_3_3_70b_versatile": "llama-3.3-70b-versatile",
            "gpt_oss_120b":"openai/gpt-oss-120b",
            "gpt_oss_20b":"openai/gpt-oss-20b"
        }
    }

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()