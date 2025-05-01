from Backend.Database.connect_mongo import get_mongo_collections
from datetime import datetime
import random

payments_collection, _ = get_mongo_collections()

def simulate_payment(method):
    """
    Simulates a payment

    Args:
        method (str): payment method

    Returns:
        str: "completed" if payment is successful, "failed" otherwise.
    """
    if method not in ["credit_card", "debit_card"]:
        print(f"Unsupported payment method: {method}")
        return "failed"
    success_rate = 0.9 if method == "credit_card" else 0.85
    return "completed" if random.random() < success_rate else "failed"

def insert_payment(user_id, amount, method, status=None, reservation_id=None):
    """
    Inserts payment record to database and returns the inserted ID if successful.

    Args:
        user_id (str): User ID
        amount (float): Payment amount.
        method (str): Payment method
        status (str, optional): Payment status.
        reservation_id (str, optional): The reservation ID.

    Returns:
        str or None: The inserted payment ID if payment is successful, otherwise None.
    """
    try:
        if status is None:
            status = simulate_payment(method)

        payment = {
            "user_id": user_id,
            "amount": round(amount, 2),
            "method": method,
            "status": status,
            "reservation_id": reservation_id,
            "date": datetime.now()
        }
        result = payments_collection.insert_one(payment)
        print(f"✅ Payment inserted (Status: {status}) - ID: {result.inserted_id}")
        return result.inserted_id if status == "completed" else None

    except Exception as e:
        print("❌ Error inserting payment:", e)
