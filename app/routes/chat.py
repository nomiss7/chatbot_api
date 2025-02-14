from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.connection import async_session
from app.models.conversation import Conversation
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.security import get_current_user
import uuid
from datetime import datetime

router = APIRouter()


@router.post("/ask/")
async def chat_ask(request: ChatRequest, user_email: str = Depends(get_current_user)):
    """Отправка сообщения в чат"""
    async with async_session() as session:
        conversation_id = request.conversation_id or str(uuid.uuid4())

        result = await session.execute(select(Conversation).filter(Conversation.conversation_id == conversation_id))
        existing_conversation = result.scalars().first()

        if existing_conversation and existing_conversation.status == "closed":
            raise HTTPException(status_code=400, detail="This conversation is closed and cannot be continued.")

        messages = [
            {"sender": "user", "message": request.message, "timestamp": datetime.utcnow()},
            {"sender": "bot", "message": "Bot response", "timestamp": datetime.utcnow()}
        ]

        if existing_conversation:
            existing_conversation.messages += messages
        else:
            new_conversation = Conversation(conversation_id=conversation_id, messages=messages, status="open")
            session.add(new_conversation)

        await session.commit()

        return ChatResponse(conversation_id=conversation_id, messages=messages, status="answer_provided")
