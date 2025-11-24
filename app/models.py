from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

# Define Expense categories as Enum
class ExpenseCategory(enum.Enum):
    Food = "Food"
    Transport = "Transport"
    Entertainment = "Entertainment"
    Utilities = "Utilities"
    Other = "Other"

# User model
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable = False)
    salary = Column(Float, default=0.0)

    # Relationship with Expense
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")

# Expense model
class Expense(Base):
    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(Enum(ExpenseCategory), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship back to User
    user = relationship("User", back_populates="expenses")
