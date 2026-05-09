# Law AI 🏛️ - Legal AI Assistant

A full-stack AI-powered legal assistant application that leverages advanced language models and web search capabilities to provide intelligent legal information and analysis. Built with FastAPI, Streamlit, and multiple LLM providers.

## 🎯 Overview

**Law Buddy** is an intelligent legal assistant designed to help users understand complex legal concepts, analyze documents, and get quick legal insights. The application features a modular architecture with:

- **Chat Interface**: Real-time conversational AI with model selection
- **Prompt Engineering**: Advanced prompt analysis and optimization
- **Multi-Model Support**: Integration with Google Gemini and Groq's LLaMA models
- **Web Search Integration**: Access to current legal information via Tavily
- **Conversation Management**: Persistent chat history with MongoDB
- **Voice Input**: Audio transcription support with Faster Whisper

## ✨ Key Features

### 1. **Intelligent Chat System**
   - Support for multiple LLM providers (Google Gemini, Groq LLaMA)
   - Conversation history tracking and management
   - Structured response formatting with emojis and markdown
   - Context-aware legal guidance

### 2. **Prompt Management**
   - Prompt quality analysis and scoring
   - Automated prompt improvement suggestions
   - Query enhancement for better results
   - Prompt optimization feedback

### 3. **Multi-Model LLM Support**
   - **Google Models**:
     - Gemini 2.5 Flash (fast, efficient)
     - Gemini 2.5 Pro (advanced reasoning)
     - Gemini Embedding models
   - **Groq Models**:
     - LLaMA 3.1 8B Instant
     - LLaMA 3.3 70B Versatile
     - OpenAI OSS models (20B, 120B)

### 4. **Data Persistence**
   - MongoDB for chat and conversation storage
   - Indexed collections for fast queries
   - Automatic conversation timestamping

### 5. **Frontend Features**
   - Streamlit-based UI
   - Real-time model selection
   - Chat history sidebar
   - Audio/voice input with transcription
   - Prompt builder dashboard

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (v0.135.2)
- **Server**: Uvicorn (v0.42.0)
- **LLM Providers**:
  - LangChain (v1.2.15) - LLM orchestration
  - LangGraph (v1.1.6) - Graph-based workflows
  - LangSmith (v0.7.26) - LLM debugging/monitoring
  - Google Generative AI (LangChain integration)
  - Groq API (LangChain integration)
- **Database**: 
  - MongoDB (v4.16.0)
  - Motor (v3.7.1) - Async MongoDB driver
- **Data Validation**: Pydantic (v2.12.5)
- **Search Integration**: Tavily API

### Frontend
- **Framework**: Streamlit (v1.55.0)
- **Audio Processing**: Faster Whisper (v1.2.1)
- **HTTP Client**: Requests (v2.32.5)

### Infrastructure
- **Environment Management**: Python-dotenv (v1.2.2)
- **Authentication**: Python-JOSE (v3.5.0)
- **ML Framework**: PyTorch (v2.11.0)
- **Document Processing**:
  - Unstructured (v0.22.23)
  - PDFMiner (v20191125)

## 📁 Project Structure

```
law_ai/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Configuration & settings
│   │   ├── components/
│   │   │   └── Input/
│   │   │       ├── basic.py         # Basic prompt template
│   │   │       ├── moderate.py      # Moderate prompt template (Law Buddy system)
│   │   │       └── copilote.py      # Copilot prompt template
│   │   ├── database/
│   │   │   ├── store/
│   │   │   │   └── mongodb.py       # MongoDB connection & operations
│   │   │   ├── vector/              # Vector DB integrations
│   │   │   │   ├── pinecone.py
│   │   │   │   └── weaviate.py
│   │   │   └── web/                 # Web search integrations
│   │   │       ├── exa.py
│   │   │       ├── firecrawl.py
│   │   │       └── tavily.py
│   │   ├── model/
│   │   │   ├── gemini.py            # Google Gemini model configuration
│   │   │   └── groq.py              # Groq LLaMA model configuration
│   │   ├── routes/
│   │   │   ├── chat.py              # Chat endpoints
│   │   │   └── prompt.py            # Prompt optimization endpoints
│   │   ├── schema/
│   │   │   ├── chat.py              # Chat input/output schemas
│   │   │   ├── conversation.py      # Conversation schemas
│   │   │   ├── copilot.py           # Copilot prompt schemas
│   │   │   └── schemas.py           # Additional schemas
│   │   └── services/
│   │       ├── chat.py              # Chat business logic
│   │       └── prompt.py            # Prompt service logic
│   └── requirements.txt
├── frontend/
│   ├── main.py                      # Streamlit UI application
│   └── requirements.txt
├── requirements.txt                 # Root dependencies
├── test.py                          # Test file
├── PRD.MD                           # Product Requirements Document
└── README.md                        # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- MongoDB instance running
- API Keys for:
  - Google Gemini API
  - Groq API
  - Tavily (optional, for web search)
  - LangChain API (optional, for monitoring)

### Installation

1. **Clone the repository**
   ```bash
   cd law_ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # source .venv/bin/activate  # On Unix
   ```

3. **Install dependencies**
   ```bash
   # Install backend dependencies
   cd backend
   pip install -r requirements.txt
   
   # Install frontend dependencies
   cd ../frontend
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # App Configuration
   APP_ENV=development
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256

   # MongoDB
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
   DB_NAME=law_ai_db

   # Google OAuth (Optional)
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
   FRONTEND_URL=http://localhost:8501

   # LLM API Keys
   GOOGLE_API_KEY=your-google-api-key
   GROQ_API_KEY=your-groq-api-key
   TAVILY_API_KEY=your-tavily-api-key

   # LangChain (Optional)
   LANGCHAIN_API_KEY=your-langchain-api-key
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_PROJECT=law-ai

   # Rate Limits
   FREE_DAILY_LIMIT=50
   PRO_DAILY_LIMIT=500
   ```

5. **Install FFmpeg** (Required for Whisper audio processing)
   ```bash
   winget install ffmpeg  # Windows
   # brew install ffmpeg  # macOS
   # sudo apt-get install ffmpeg  # Linux
   ```

### Running the Application

1. **Start the Backend API**
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the Frontend** (in a new terminal)
   ```bash
   cd frontend
   streamlit run main.py
   ```

3. **Access the Application**
   - Frontend: http://localhost:8501
   - API Docs: http://localhost:8000/docs
   - API RedDocs: http://localhost:8000/redoc

## 🔌 API Endpoints

### Chat Endpoints

**POST /chat** - Send a message and get AI response
```json
Request:
{
  "prompt": "What is contract law?",
  "model": "gemini_2_5_flash",
  "chat_id": null  // optional, for continuing conversations
}

Response:
{
  "response": "Contract law is...",
  "chat_id": "507f1f77bcf86cd799439011",
  "history": [...]
}
```

**GET /chat/conversations** - Get all conversations
```json
Response:
{
  "chat_history": [
    {
      "chat_id": "...",
      "title": "First message",
      "model": "gemini_2_5_flash",
      "created_at": "...",
      "updated_at": "..."
    }
  ]
}
```

**GET /chat/messages/{chat_id}** - Get messages from a conversation
```json
Response:
{
  "chat_id": "507f1f77bcf86cd799439011",
  "messages": [
    {
      "message_id": "...",
      "role": "user",
      "content": "...",
      "qna_id": "...",
      "timestamp": "..."
    }
  ]
}
```

**DELETE /chat/conversations/{chat_id}** - Delete a conversation

### Prompt Endpoints

**POST /prompt/copilot** - Get prompt analysis and suggestions
```json
Request:
{
  "prompt": "Your prompt here"
}

Response:
{
  "predicted_goal": "...",
  "prompt_quality_score": 0-100,
  "score_reason": "...",
  "missing_areas": [...],
  "questions": [...],
  "suggestions": [...],
  "is_ready": true/false
}
```

### Health & System

**GET /** - Welcome message
**GET /health** - Health check
**GET /models** - Get available models

## 📊 Configuration

### Available Models

The application supports the following LLM models:

**Google Models:**
- `gemini_2_5_flash` - Fast model for quick responses
- `gemini_2_5_pro` - Advanced model for complex reasoning
- Embedding models for semantic search

**Groq Models:**
- `llama_3_1_8b_instant` - Smaller model for quick inference
- `llama_3_3_70b_versatile` - Larger model for better quality
- OpenAI OSS variants

### Response Formatting

The system uses the "moderate" prompt template which enforces:
- Structured markdown responses with clear headings
- Strategic emoji usage for readability
- Code blocks with language specification
- Bullet points for lists
- Conversational yet professional tone

## 🗂️ Database Schema

### Collections

**chats** - Conversation metadata
```json
{
  "_id": ObjectId,
  "title": "string",
  "model": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**messages** - Chat messages and responses
```json
{
  "_id": ObjectId,
  "chat_id": ObjectId,
  "qna_id": ObjectId,
  "model": "string",
  "role": "user|assistant",
  "content": "string",
  "timestamp": "datetime"
}
```

### Indexes
- `chats.chat_id` for fast lookups
- `messages.(chat_id, role, created_at)` for efficient message retrieval

## 🎨 Frontend Features (Streamlit)

The Streamlit frontend includes:

- **Model Selection** - Choose between available LLM providers and models
- **Chat Interface** - Real-time messaging with conversation history
- **Sidebar Navigation** - Access to previous conversations
- **Audio Input** - Voice transcription using Faster Whisper
- **Prompt Builder** - Tools for optimizing prompts
- **Session State Management** - Persistent state across reruns

## 🔧 Development Notes

### Adding New Features

1. **Adding a New LLM Provider**
   - Create model integration in `backend/app/model/`
   - Update `config.py` with available models
   - Add model selection logic in `services/chat.py`

2. **Adding Web Search Integration**
   - Implement search service in `backend/app/database/web/`
   - Integrate with prompt enhancement pipeline

3. **Adding Vector Database**
   - Implement vector store in `backend/app/database/vector/`
   - Integrate embeddings from Gemini or other providers

### Prompt Engineering

The system includes three prompt templates:
- `basic.py` - Simple template for basic queries
- `moderate.py` - **Current default** - Structured formatting with Law Buddy persona
- `copilote.py` - Advanced copilot-style prompts

Current prompt focuses on:
- Emoji-enhanced readability
- Structured markdown formatting
- Legal expertise tone
- Educational approach with examples

### Debugging & Monitoring

- LangSmith integration for LLM call tracing
- FastAPI automatic API documentation at `/docs`
- MongoDB query indexing for performance
- Async operations for scalability

## ⚠️ Important Features in Development

- Query enhancement and transformation
- Web search integration (Tavily, Exa, Firecrawl)
- Vector database support (Pinecone, Weaviate)
- Document analysis and PDF processing
- Authentication system
- Usage quota management (FREE_DAILY_LIMIT, PRO_DAILY_LIMIT)

## 📝 License

This project is under development. Check with the maintainer for licensing information.

## 🤝 Contributing

To contribute to this project:

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📧 Support

For issues and questions, please refer to the GitHub issues or contact the development team.