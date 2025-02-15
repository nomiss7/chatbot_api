from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.connection import async_session
from app.models.conversation import Conversation
from app.core.security import get_current_user

router = APIRouter()


@router.get("/conversations/")
async def list_conversations(user_email: str = Depends(get_current_user)):
    async with async_session() as session:
        result = await session.execute(select(Conversation))
        conversations = result.scalars().all()

        return {"conversations": conversations}


@router.get("/conversations/{conversation_id}/")
async def get_conversation(conversation_id: str, user_email: str = Depends(get_current_user)):
    async with async_session() as session:
        result = await session.execute(
            select(Conversation).filter(Conversation.conversation_id == conversation_id)
        )
        conversation = result.scalars().first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        return {
            "conversation_id": conversation.conversation_id,
            "status": conversation.status,
            "messages": conversation.messages
        }
