"""
Reservation availability

Provides utility functions:
- Checks if parking spot is avail.
- Makr expired reservations in the database.

Dependencies:
    - pymongo: MongoDB 
    - datetime: time
    - time: updates
"""

from Backend.Database.connect_mongo import get_mongo_collections
from datetime import timedelta, datetime
import time

_, reservations_collection = get_mongo_collections()

def is_spot_available(parking_spot, start_time, duration_minutes):
    """
    Checks if parking spot is avail

    Args:
        parking_spot (str): Lot ID.
        start_time (datetime): Start time
        duration_minutes (int): Reserve time

    Returns:
        bool: 
    """
    try:
        end_time = start_time + timedelta(minutes=duration_minutes)

        overlapping_reservations = list(reservations_collection.find({
            "parking_spot": parking_spot,
            "$or": [
                {
                    "reservation_time": {"$lt": end_time},
                    "end_time": {"$gt": start_time}
                }
            ],
            "status": {"$in": ["active", "upcoming"]}
        }))

        return len(overlapping_reservations) == 0

    except Exception as e:
        print("Verification error for availability:", e)
        return False

def update_expired_reservations():
    """
    Marks all expired reservations.

    A reservation is considered expired if:
        - Its end_time is in the past

    Side Effects:
        - Prints the number of reservations updated.
    """
    try:
        now = datetime.now()
        result = reservations_collection.update_many(
            {
                "end_time": {"$lte": now},
                "status": {"$in": ["active", "upcoming"]}
            },
            {"$set": {"status": "expired"}}
        )
        print(f"{result.modified_count} expired reservation(s).")
    except Exception as e:
        print("Error during reservation update:", e)

def run_auto_update(interval_seconds=60):
    """
    Runs updates to expire reservations.

    Args:
        interval_seconds (int): Seconds.

    Behavior:
        - Calls update_expired_reservations().
    """
    print("Auto-update. Verifications every", interval_seconds, "secondes.")
    while True:
        update_expired_reservations()
        time.sleep(interval_seconds)
