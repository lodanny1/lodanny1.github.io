from Backend.Database.connect_mongo import get_mongo_collections
from datetime import datetime, timedelta
from  Backend.Logic.check_availability import is_spot_available

_, reservations_collection = get_mongo_collections()

def insert_reservation(user_id, parking_spot, reservation_time, duration_minutes, payment_id=None, status="active"):
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

