from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://chatbot:7@localhost/chatbot_db")
DATABASE_URL = "postgresql+asyncpg://chatbot:CpyZoSp796pSjuOqCBKNYhiG3T0mRQlA@dpg-cunti4dumphs73bqdgog-a.oregon-postgres.render.com/chatbot_db_spgr"

async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
