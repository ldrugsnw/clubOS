from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    transaction_date: datetime
    description: str
    transaction_type: Optional[str] = None
    institution: Optional[str] = None
    account_number: Optional[str] = None
    amount: int  # 원 단위
    balance: int  # 원 단위
    memo: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    transaction_type: Optional[str] = None
    institution: Optional[str] = None
    account_number: Optional[str] = None
    amount: Optional[int] = None
    balance: Optional[int] = None
    memo: Optional[str] = None

class Transaction(TransactionBase):
    id: str
    file_name: Optional[str] = None
    uploaded_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TransactionStats(BaseModel):
    total_balance: int
    this_term_income: int
    this_term_expense: int
    this_term_profit: int
    previous_balance: int
    total_transactions: int
    latest_transaction_date: Optional[datetime]