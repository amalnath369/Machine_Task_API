from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from schemas import ExpenseCreate, ExpenseRead
from crud import create_expense, get_expenses, get_budget_summary
from database import get_db
from models import ExpenseCategory
from security import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseRead)
async def api_create_expense(expense: ExpenseCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if expense.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    return await create_expense(db, expense)

@router.get("/{user_id}", response_model=List[ExpenseRead])
async def api_get_expenses(
    user_id: int,
    day: Optional[str]=None,
    week: Optional[int]=None,
    month: Optional[int]=None,
    year: Optional[int]=None,
    category: Optional[ExpenseCategory]=None,
    db: AsyncSession=Depends(get_db),
    current_user=Depends(get_current_user)
):
    if user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    return await get_expenses(db, user_id, day, week, month, year, category)

@router.get("/totals/{user_id}")
async def budget_summary(user_id: int, db: AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    if user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    summary = await get_budget_summary(db, user_id)
    if not summary:
        raise HTTPException(status_code=404, detail="User not found")
    return summary
