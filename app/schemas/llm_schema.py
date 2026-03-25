from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    reply: str

class HistoryItem(BaseModel):
    role: str
    content: str

class ChatStreamRequest(BaseModel):
    prompt: str
    history: Optional[List[HistoryItem]] = []
