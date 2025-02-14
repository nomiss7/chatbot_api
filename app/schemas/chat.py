from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ChatMessage(BaseModel):
    sender: str
    message: str
    timestamp: datetime

class ChatRequest(BaseModel):
    conversation_id: Optional[str]
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    messages: List[ChatMessage]
    status: str
