from pydantic_settings.sources.providers import aws
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime, timezone
from app.config import settings
from app.model.gemini import get_gemini_model
from app.model.groq import get_groq_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.schema.chat import ChatInput, ChatResponse, MessagesResponse
from app.schema.conversation import ConversationResponse
# from app.components.Input.basic import prompt
from app.components.Input.moderate import prompt
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

def build_history(history: list[dict]) -> list[dict]:
    messages = []
    exit_messages = []
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
            exit_messages.append({"role": msg["role"], "content": msg["content"], "qna_id": str(msg["qna_id"])})
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
            exit_messages.append({"role": msg["role"], "content": msg["content"], "qna_id": str(msg["qna_id"])})
    return messages, exit_messages
    
class ChatService:
    def __init__(self, db):
        self.db = db

    async def handel_chates(self, chat_input: ChatInput) -> ChatResponse:
        llm = get_llm(chat_input.model)

        if chat_input.chat_id is None:
            response = await self.db["chats"].insert_one({
                "title": chat_input.prompt,
                "model": chat_input.model,
                "created_at": utc_now(),
                "updated_at": utc_now()
            })
            chat_id = response.inserted_id
        else:
            chat_id = _validate_chat_id(chat_input.chat_id)
            if not await self.db["chats"].find_one({"_id": chat_id}):
                raise HTTPException(status_code=404, detail="Chat not found")

        try:
            conversation_history = await self.db["messages"].find({"chat_id": chat_id}).sort("created_at", 1).to_list()
            history, exit_messages = build_history(conversation_history)
            chain = prompt | llm | StrOutputParser()
            ai_response = chain.invoke({"history": history, "question": chat_input.prompt})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in LLM: {str(e)}")
            
        qna_id = ObjectId()
        await self.db["messages"].insert_many([
            {"chat_id": chat_id, "qna_id": qna_id, "model": chat_input.model, "role": "user", "content": chat_input.prompt, "timestamp": utc_now()},
            {"chat_id": chat_id, "qna_id": qna_id, "model": chat_input.model, "role": "assistant", "content": ai_response, "timestamp": utc_now()}
        ])
        await self.db["chats"].update_one(
            {"_id": chat_id}, {"$set": {"updated_at": utc_now()}}
            )

        updated_history = exit_messages + [
            {"role": "user", "content": chat_input.prompt, "qna_id": str(qna_id)}, 
            {"role": "assistant", "content": ai_response, "qna_id": str(qna_id)}
        ]
        # print(updated_history)
        return ChatResponse(
            response=ai_response,
            chat_id=str(chat_id),
            history=updated_history
        )

    async def get_conversations(self) -> ConversationResponse:
        try:
            conversations = await self.db["chats"].find().sort("created_at", -1).to_list(100)
            print(conversations)
            for conversation in conversations:
                conversation["chat_id"] = str(conversation.pop("_id"))
                conversation["created_at"] = str(conversation["created_at"])
                conversation["updated_at"] = str(conversation["updated_at"])
            return ConversationResponse(chat_history=conversations) 
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in fetching conversations: {str(e)}")

    async def get_messages(self, chat_id: str) -> MessagesResponse:
        try:
            chat_id = _validate_chat_id(chat_id)
            messages = await self.db["messages"].find({"chat_id": chat_id}).sort("timestamp", 1).to_list()
            print(messages)
            for message in messages:
                message["message_id"] = str(message.pop("_id"))
                message["qna_id"] = str(message.pop("qna_id"))
            return MessagesResponse(chat_id=str(chat_id), messages=messages)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in fetching messages: {str(e)}")

    async def delete_conversation(self, chat_id: str) -> dict:
        try:
            chat_id = _validate_chat_id(chat_id)
            messages = await self.db["messages"].delete_many({"chat_id": chat_id})
            chat = await self.db["chats"].delete_one({"_id": chat_id})
            return {"messages": messages.deleted_count, "chat": chat.deleted_count}
        except HTTPException:
            raise   
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in deleting message: {str(e)}") 
        