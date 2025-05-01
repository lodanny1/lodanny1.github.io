from pymongo import MongoClient
import certifi
from datetime import datetime

uri = "mongodb+srv://Skullgame300:Skullgame300@parking.v4glm.mongodb.net/?retryWrites=true&w=majority&appName=Parking"
client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())
reservations_collection = client["parking_db"]["reservations"]
spots_collection = client["parking_db"]["parking_spots"]

def update_expired_reservations():
    now = datetime.now()

    result = reservations_collection.update_many(
        {"end_time": {"$lt": now}, "status": {"$in": ["active", "upcoming"]}},
        {"$set": {"status": "expired"}}
    )
    print(f"🔁 Expired reservations updated: {result.modified_count}")

    expired_spots = reservations_collection.find({"status": "expired"})
    expired_spot_ids = [r["parking_spot"] for r in expired_spots]

    if expired_spot_ids:
        spots_collection.update_many(
            {"spot_id": {"$in": expired_spot_ids}},
            {"$set": {"status": "available"}}
        )
        print(f"✅ Spot statuses updated to 'available': {len(expired_spot_ids)}")