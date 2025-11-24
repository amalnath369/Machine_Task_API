from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User, Expense, ExpenseCategory
from schemas import UserCreate, ExpenseCreate
from security import hash_password
from typing import List, Optional
from datetime import datetime, timedelta

# Create user
async def create_user(db: AsyncSession, user: UserCreate, password: str):
    db_user = User(
        username=user.username,
        salary=user.salary,
        hashed_password=hash_password(password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Get user by username
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

# Authenticate user
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    from security import verify_password
    if not verify_password(password, user.hashed_password):
        return None
    return user

# Create expense
async def create_expense(db: AsyncSession, expense: ExpenseCreate):
    db_expense = Expense(
        user_id=expense.user_id,
        name=expense.name,
        amount=expense.amount,
        category=expense.category
    )
    db.add(db_expense)
    await db.commit()
    await db.refresh(db_expense)
    return db_expense

# Get expenses with filters
async def get_expenses(db: AsyncSession, user_id: int, day: Optional[str]=None,
                       week: Optional[int]=None, month: Optional[int]=None,
                       year: Optional[int]=None, category: Optional[ExpenseCategory]=None):
    stmt = select(Expense).where(Expense.user_id == user_id)

    if day:
        start = datetime.strptime(day, "%Y-%m-%d")
        end = start + timedelta(days=1)
        stmt = stmt.where(Expense.created_at >= start, Expense.created_at < end)
    
    if week and year:
        first_day = datetime.strptime(f'{year}-01-01', "%Y-%m-%d")
        start = first_day + timedelta(days=(week-1)*7)
        end = start + timedelta(days=7)
        stmt = stmt.where(Expense.created_at >= start, Expense.created_at < end)
    
    if month and year:
        start = datetime(year, month, 1)
        end = datetime(year, month+1, 1) if month < 12 else datetime(year+1, 1, 1)
        stmt = stmt.where(Expense.created_at >= start, Expense.created_at < end)
    
    if category:
        stmt = stmt.where(Expense.category == category)
    
    result = await db.execute(stmt)
    return result.scalars().all()

# Budget summary
async def get_budget_summary(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return None

    expenses_stmt = await db.execute(select(Expense).where(Expense.user_id==user_id))
    expenses = expenses_stmt.scalars().all()
    total_expense = sum(e.amount for e in expenses)
    remaining = user.salary - total_expense
    category_breakdown = {cat.value: sum(e.amount for e in expenses if e.category==cat) for cat in ExpenseCategory}
    return {
        "total_expense": total_expense,
        "total_salary": user.salary,
        "remaining_amount": remaining,
        "category_breakdown": category_breakdown
    }
