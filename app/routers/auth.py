from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserLogin, Token
from crud import authenticate_user, create_user
from database import get_db
from security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=Token)
async def signup(username: str, password: str, db: AsyncSession = Depends(get_db)):
    user = await create_user(db, username=username, password=password, user={"username": username, "salary":0})
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    authenticated = await authenticate_user(db, user.username, user.password)
    if not authenticated:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": authenticated.username})
    return {"access_token": token, "token_type": "bearer"}
