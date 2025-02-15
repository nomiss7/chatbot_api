from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.connection import async_engine, async_session
from app.routes import auth, chat, history


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(lambda _: None)
    try:
        yield
    finally:
        await async_session().close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(chat.router, prefix="/api/chatbot", tags=["Chat"])
app.include_router(history.router, prefix="/api/chatbot", tags=["Chat History"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0")
