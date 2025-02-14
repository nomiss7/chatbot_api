from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.connection import async_session
from app.models.conversation import Conversation
from app.core.security import get_current_user

router = APIRouter()


@router.post("/conversations/{conversation_id}/close/")
async def close_conversation(conversation_id: str, user_email: str = Depends(get_current_user)):
    """Закрытие чата"""
    async with async_session() as session:
        result = await session.execute(select(Conversation).filter(Conversation.conversation_id == conversation_id))
        conversation = result.scalars().first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        conversation.status = "closed"
        await session.commit()

        return {"message": "Conversation has been closed.", "conversation_id": conversation_id, "status": "closed"}
