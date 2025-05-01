"""
Reservation insertion logic for Parking App.

Provides functionality to insert new parking reservations in MongoDB database.
It ensures spot is avail before.

Functions:
    insert_reservation: Inserts a reservation document into database.
"""

from Backend.Database.connect_mongo import get_mongo_collections
from datetime import datetime, timedelta
from Backend.Logic.check_availability import is_spot_available

_, reservations_collection = get_mongo_collections()

def insert_reservation(user_id, parking_spot, reservation_time, duration_minutes, payment_id=None, status="active"):
    """
    Insert a new reservation into the database after checking availability.

    Args:
        user_id (str): User ID
        parking_spot (str): ParkingSpot ID
        reservation_time (datetime): Start Time
        duration_mnutes (int): Length of reservation
        payment_id (str, optional): Payment id
        status (str, optional): Reservation status

    Returns:
        ObjectId or None: The MongoDB ID of reservation if successful

    Raises:
        Exception: During the insertion
    """
    try:
        end_time = reservation_time + timedelta(minutes=duration_minutes)

        if not is_spot_available(parking_spot, reservation_time, duration_minutes):
            print("❌ Parking spot is already reserved.")
            return None

        reservation = {
            "user_id": user_id,
            "parking_spot": parking_spot,
            "reservation_time": reservation_time,
            "duration_minutes": duration_minutes,
            "end_time": end_time,
            "payment_id": payment_id,
            "status": status,
            "created_at": datetime.now()
        }

        result = reservations_collection.insert_one(reservation)
        print(f"✅ Reservation inserted - ID: {result.inserted_id}")
        return result.inserted_id

    except Exception as e:
        print("❌ Error during reservation:", e)
        return None
