"""
Fetches and formats user payment history.

Connects to the MongoDB , retrieves the payment records. 
"""

from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import certifi

def get_user_payment_history(username):
    """
    Retrieves user's payment history from the MongoDB database.

    For each payment, it includes:
        - Payment date
        - Amount
        - Payment method
        - Associated reservation spot and time
        - Payment status

    Args:
        username (str): Username.

    Returns:
        str: String of user's payment history.
            
    """
    uri = "mongodb+srv://Skullgame300:Skullgame300@parking.v4glm.mongodb.net/?retryWrites=true&w=majority&appName=Parking"
    client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())
    db = client["parking_db"]
    payments = db["payments"]
    reservations = db["reservations"]

    records = payments.find({"user_id": username}).sort("date", -1)
    text = ""

    for payment in records:
        res_time = "-"
        spot = "-"
        if payment.get("reservation_id"):
            res = reservations.find_one({"_id": payment["reservation_id"]})
            if res:
                res_time = res.get("reservation_time", "-")
                if isinstance(res_time, datetime):
                    res_time = res_time.strftime("%Y-%m-%d %H:%M")
                spot = res.get("parking_spot", "-")

        text += (
            f"Date: {payment['date'].strftime('%Y-%m-%d %H:%M')}\n"
            f"Amount: €{payment['amount']}\n"
            f"Method: {payment['method']}\n"
            f"Reservation: {spot} at {res_time}\n"
            f"Status: {payment['status']}\n"
            f"{'-'*40}\n"
        )

    return text if text else "No payments found."
