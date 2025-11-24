from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ExpenseCategory(str, Enum):
    Food = "Food"
    Transport = "Transport"
    Entertainment = "Entertainment"
    Utilities = "Utilities"
    Other = "Other"

# ----------------- User Schemas -----------------

class UserBase(BaseModel):
    username: str = Field(..., example="john_doe")
    salary: Optional[float] = Field(default=0.0, example=5000.0)

class UserCreate(UserBase):
    pass  

class UserRead(UserBase):
    user_id: int

    class Config:
        orm_mode = True  # Needed for ORM models to work with Pydantic

# ----------------- Expense Schemas -----------------

class ExpenseBase(BaseModel):
    name: str = Field(..., example="Lunch")
    amount: float = Field(..., gt=0, example=150.0)  # amount must be >0
    category: ExpenseCategory = Field(..., example="Food")

class ExpenseCreate(ExpenseBase):
    user_id: int  # FK reference for creation

class ExpenseRead(ExpenseBase):
    expense_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Optional: User with Expenses (nested)
class UserWithExpenses(UserRead):
    expenses: List[ExpenseRead] = []


# For authentication
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str
