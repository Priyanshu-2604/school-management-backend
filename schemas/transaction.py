# app/schemas/transaction.py

from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class TransactionItem(BaseModel):
    id: int
    student_name: str
    amount: float
    payment_type: str
    payment_method: str
    date: datetime
    status: str

class TransactionSummary(BaseModel):
    total_amount: float
    transaction_count: int
    average_amount: float

class TransactionReport(BaseModel):
    summary: TransactionSummary
    payment_breakdown: Dict[str, Dict[str, float]]
    transactions: List[TransactionItem]
