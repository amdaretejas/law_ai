from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


client = None
db     = None


async def connect_db():
    global client, db
    client = AsyncIOMotorClient(
        settings.MONGODB_URL,
        tls=True,
        tlsAllowInvalidCertificates=False,
        serverSelectionTimeoutMS=30000
    )
    db = client[settings.DB_NAME]
    await client.admin.command("ping")
    await db.chats.create_index([('chat_id', 1)])
    await db.messages.create_index([('chat_id', 1), ('role', 1), ('created_at', 1)])

async def disconnect_db():
    global client
    if client:
        client.close()

def get_db():
    return db