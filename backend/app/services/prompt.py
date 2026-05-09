import json
from pydantic_settings.sources.providers import aws
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime, timezone
from app.config import settings
from app.model.gemini import get_gemini_model
from app.model.groq import get_groq_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.schema.chat import ChatInput, ChatResponse, MessagesResponse
from app.schema.copilot import PromptCopilotInput, PromptCopilotResponse
from app.components.Input.copilote import prompt
from langchain_core.output_parsers import StrOutputParser

def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)

def _validate_chat_id(chat_id: str) -> ObjectId:
    if not ObjectId.is_valid(chat_id):
        raise HTTPException(status_code=400, detail="Invalid Chat ID")

    return ObjectId(chat_id)

def get_llm(model: str):
    if model in settings.AVAILABLE_MODELS.get("google", []):
        return get_gemini_model(model)
    if model in settings.AVAILABLE_MODELS.get("groq", []):
        return get_groq_model(model)
    raise HTTPException(status_code=400, detail=f"Model '{model}' is not supported.")

class PromptService:
    def __init__(self, db):
        self.db = db

    async def get_copilot(self, prompt_input: PromptCopilotInput):
        llm = get_llm(prompt_input.model)
        try:
            structured_llm = llm.with_structured_output(
                PromptCopilotResponse
            )
            chain = prompt | structured_llm
            response = chain.invoke({
            "original_prompt": prompt_input.original_prompt,
            "previous_prompt": prompt_input.previous_prompt,
            "current_prompt": prompt_input.current_prompt,
            "original_score": prompt_input.original_score,
            "previous_score": prompt_input.previous_score,
            "history": prompt_input.history
            })
            print(response)
            return response
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error in LLM: {str(e)}"
            )