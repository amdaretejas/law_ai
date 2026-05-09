from fastapi import APIRouter, Depends
from app.database.store.mongodb import get_db
from app.schema.copilot import PromptCopilotInput, PromptCopilotResponse
from app.services.prompt import PromptService

router = APIRouter(prefix="/prompt", tags=["Prompt"])

def get_chat_services(db=Depends(get_db)) -> PromptService:
    return PromptService(db)

@router.post("/copilot", response_model=PromptCopilotResponse)
async def copilot(prompt_input: PromptCopilotInput, prompt_service: PromptService = Depends(get_chat_services)):
    return await prompt_service.get_copilot(prompt_input)