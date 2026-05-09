from fastapi import APIRouter, Depends
from app.database.store.mongodb import get_db
from app.schema.chat import ChatInput, ChatResponse, MessagesResponse
from app.schema.conversation import ConversationDict, ConversationResponse
from app.services.chat import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

def get_chat_services(db=Depends(get_db)) -> ChatService:
    return ChatService(db)

@router.post("/", response_model=ChatResponse)
async def chat(chat_input: ChatInput, chat_services: ChatService = Depends(get_chat_services)):
    return await chat_services.handel_chates(chat_input)

@router.get("/conversations", response_model=ConversationResponse)
async def get_conversations(chat_services: ChatService = Depends(get_chat_services)):
    return await chat_services.get_conversations()

@router.get("/messages/{chat_id}", response_model=MessagesResponse)
async def get_messages(chat_id: str, chat_services: ChatService = Depends(get_chat_services)):
    return await chat_services.get_messages(chat_id)

@router.delete("/conversations/{chat_id}")
async def delete_conversation(chat_id: str, chat_services: ChatService = Depends(get_chat_services)):
    return await chat_services.delete_conversation(chat_id)
