from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager
from app.config import settings
from app.routes import chat
from app.routes import prompt
from app.database.store.mongodb import connect_db, disconnect_db

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()

app = FastAPI(
    title="Law AI",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "https://*.streamlit.app",
        settings.FRONTEND_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(prompt.router)
# app.include_router(history.router)
# app.include_router(pdf.router)


@app.get("/")
def root():
    return {"message": "Welcome to Law AI"}

@app.get("/health")
async def health():
    return {"status": "ok", "app": "Law AI", "version": "1.0.0"}


@app.get("/models")
async def get_models():
    return {"models": settings.AVAILABLE_MODELS}