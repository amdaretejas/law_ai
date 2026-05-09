from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer in 2 sentences max."),
    MessagesPlaceholder("history"),
    ("human", "{question}")
])