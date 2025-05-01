"""
Handles payment and reservation logic.

Processes both the payment and insertion of parking reservation.
Ensures reservation time doesn't conflict with existing ones, updates expired reservations,
calculates cost, and inserts the related documents into MongoDB.

Functions:
    make_reservation_with_payment: Creates reservation with payment validation.
"""

from datetime import datetime, timedelta
from Backend.Database.connect_mongo import get_mongo_collections
from Backend.Logic.insert_payment import insert_payment
from Backend.Logic.check_availability import update_expired_reservations
from Backend.Logic.pricing import calculate_price
from pymongo import ReturnDocument

# Get collections
payments_collection, reservations_collection = get_mongo_collections()

def make_reservation_with_payment(parking_spot, reservation_time, duration_minutes, amount, method, user_id):
    """
    Reserves parking spots with payment

    Args:
        parking_spot (str):Parking ID.
        reservation_time (datetime): Start time reservation.
        duration_minutes (int): Duration of the reservations.
        amount (float): Placeholder.
        method (str): Payment method.
        user_id (str): User ID.

    Returns:
        ObjectId or None: The reservation ID if successful.

    Process:
        1. Expired reservations updated.
        2. Price calculated.
        3. Payment recorded using the provided method.
        4. Reservation time checked for overlap.
        5. Reservation is stored in the database.

    Fails if:
        - Payment insertion fails.
        - The spot is already reserved.
        - Any database error.

    Raises:
        Logs and returns None.
    """
    try:
        update_expired_reservations()

        end_time = reservation_time + timedelta(minutes=duration_minutes)
        amount = calculate_price(duration_minutes)

        payment_id = insert_payment(user_id, amount, method, status="completed")
        if not payment_id:
            print("❌ Payment failed. Cancelling reservation.")
            return None

        reservation_data = {
            "user_id": user_id,
            "parking_spot": parking_spot,
            "reservation_time": reservation_time,
            "duration_minutes": duration_minutes,
            "end_time": end_time,
            "payment_id": payment_id,
            "status": "active",
            "created_at": datetime.now()
        }

        existing_conflicts = reservations_collection.find_one({
            "parking_spot": parking_spot,
            "status": {"$in": ["active", "upcoming"]},
            "reservation_time": {"$lt": end_time},
            "end_time": {"$gt": reservation_time}
        })

        if existing_conflicts:
            print(f"❌ Spot {parking_spot} is already reserved in that time slot.")
            return None

        result = reservations_collection.insert_one(reservation_data)

        if result.inserted_id:
            print(f"✅ Reservation confirmed. ID: {result.inserted_id}")
            return result.inserted_id
        else:
            print("❌ Failed to insert reservation.")
            return None

    except Exception as e:
        print("Error during reservation with payment:", e)
        return None
