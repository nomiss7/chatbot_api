from sqlalchemy import Column, String, JSON
from app.database.connection import Base


class Conversation(Base):
    __tablename__ = "conversations"

    conversation_id = Column(String, primary_key=True, index=True)
    messages = Column(JSON)
    status = Column(String, default="open")
