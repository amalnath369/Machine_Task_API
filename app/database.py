from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # True for debug, False in production
    future=True
)

# Async session
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base model for declarative
Base = declarative_base()

# Dependency for FastAPI

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session