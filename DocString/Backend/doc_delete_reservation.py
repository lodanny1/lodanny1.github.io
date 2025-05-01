from Backend.Database.connect_mongo import get_mongo_collections
from bson.objectid import ObjectId
from pymongo import MongoClient
import certifi

_, reservations_collection = get_mongo_collections()
uri = "mongodb+srv://flavienmaameri57:DCU9o2Vg0K8PvjnG@parking.v4glm.mongodb.net/?retryWrites=true&w=majority&appName=Parking"
client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())
db = client["parking_db"]
spots_collection = db["parking_spots"]

def list_reservations():
    """
    Listsreservations with index to make deletion easier.
    """
    try:
        reservations = list(reservations_collection.find())
        print("\n--- Reservations ---")
        for i, res in enumerate(reservations):
            print(f"[{i}] {res.get('parking_spot')} | {res.get('reservation_time')} | {res.get('status')} | ID: {res.get('_id')}")
        return reservations
    except Exception as e:
        print("❌ Error while listing reservations:", e)
        return []

def cancel_reservation_by_id(reservation_id):
    """
    Cancels reservation to set the parking spot to available.
    
    Args:
        reservation_id (str): The ID of the reservation

    Returns:
        None
    """
    try:
        reservation = reservations_collection.find_one({"_id": ObjectId(reservation_id)})
        if not reservation:
            print(f"❌ No reservation found with ID: {reservation_id}")
            return

        result = reservations_collection.update_one(
            {"_id": ObjectId(reservation_id)},
            {"$set": {"status": "cancelled"}}
        )

        if result.modified_count == 1:
            spot_id = reservation.get("parking_spot")
            if spot_id:
                spots_collection.update_one(
                    {"spot_id": spot_id},
                    {"$set": {"status": "available"}}
                )
                print(f"✅ Reservation {reservation_id} cancelled and spot {spot_id} is now available.")
            else:
                print("⚠️ Reservation has no associated spot_id.")
        else:
            print(f"❌ Failed to cancel reservation {reservation_id}")
    except Exception as e:
        print("❌ Error while cancelling reservation:", e)
