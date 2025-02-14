from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.connection import async_session
from app.models.user import User
from app.schemas.auth import UserRegister, UserVerify, UserLogin, Token
from app.core.security import get_current_user
import uuid
from datetime import timedelta
from app.core.security import create_access_token

router = APIRouter()


@router.post("/register/")
async def register_user(user: UserRegister):
    """Регистрация пользователя"""
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.email == user.email))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        verification_code = str(uuid.uuid4())[:6]
        new_user = User(username=user.username, email=user.email, password=user.password, verified=False,
                        verification_code=verification_code)

        session.add(new_user)
        await session.commit()

        return {"id": new_user.id, "username": user.username, "email": user.email, "verification_status": "pending",
                "message": "A verification code has been sent to your email."}


@router.post("/verify/")
async def verify_user(user: UserVerify):
    """Подтверждение кода регистрации"""
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.email == user.email))
        db_user = result.scalars().first()

        if not db_user or db_user.verification_code != user.verification_code:
            raise HTTPException(status_code=400, detail="Invalid verification code")

        db_user.verified = True
        await session.commit()

        access_token = await create_access_token({"sub": user.email}, timedelta(minutes=30))

        return {"message": "Account successfully verified.", "token": access_token}


@router.post("/login/")
async def login_user(user: UserLogin):
    """Аутентификация пользователя"""
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.email == user.email))
        db_user = result.scalars().first()

        if not db_user or not db_user.verified or db_user.password != user.password:
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        access_token = await create_access_token({"sub": user.email}, timedelta(minutes=30))
        return {"token": access_token, "user_id": db_user.id}


@router.post("/logout/")
async def logout_user(user_email: str = Depends(get_current_user)):
    """Выход пользователя"""
    return {"message": "Successfully logged out."}


@router.post("/token-refresh/")
async def refresh_token(token: Token, user_email: str = Depends(get_current_user)):
    """Обновление JWT токена"""
    new_token = await create_access_token({"sub": user_email}, timedelta(minutes=30))
    return {"token": new_token}
