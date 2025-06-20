# app/api/transactions.py

from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.dependencies import get_db, get_current_user
from app.db.models import Transaction, Student
from app.core.logger import logger

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/report")
def get_transactions_report(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    class_id: Optional[str] = Query(None),
    payment_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(Transaction).join(Student)
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    if class_id:
        query = query.filter(Student.class_id == class_id)
    if payment_type:
        query = query.filter(Transaction.payment_type == payment_type)

    transactions = query.all()
    total_amount = sum(t.amount for t in transactions)
    count = len(transactions)
    avg_amount = total_amount / count if count else 0

    payment_summary = {}
    for t in transactions:
        pt = t.payment_type
        if pt not in payment_summary:
            payment_summary[pt] = {"count": 0, "amount": 0}
        payment_summary[pt]["count"] += 1
        payment_summary[pt]["amount"] += t.amount

    logger.info(f"Transaction report accessed by {current_user.username}")

    return {
        "summary": {
            "total_amount": total_amount,
            "transaction_count": count,
            "average_amount": round(avg_amount, 2)
        },
        "payment_breakdown": payment_summary,
        "transactions": [
            {
                "id": t.id,
                "student_name": t.student.name,
                "amount": t.amount,
                "payment_type": t.payment_type,
                "payment_method": t.payment_method,
                "date": t.transaction_date,
                "status": t.status
            } for t in transactions[:100]
        ]
    }
