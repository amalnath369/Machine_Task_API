from fastapi import FastAPI
from database import engine, Base
from routers import auth, expenses
from config import settings

app = FastAPI(title=settings.TITLE)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)
app.include_router(expenses.router)
