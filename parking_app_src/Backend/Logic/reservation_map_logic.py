from pymongo import MongoClient
import certifi

# MongoDB connection setup
uri = "mongodb+srv://Skullgame300:Skullgame300@parking.v4glm.mongodb.net/?retryWrites=true&w=majority&appName=Parking"
client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())
db = client["parking_db"]
spots_collection = db["parking_spots"]


def fetch_spots():
    """
    Fetch all parking spots from the database, sorted by lot and number.
    Returns a list of dicts with spot info.
    """
    try:
        spots = list(spots_collection.find({}, {"_id": 0, "spot_id": 1, "status": 1, "lot_name": 1}))
        spots.sort(key=lambda x: (x["lot_name"], int(x["spot_id"][1:])))
        return spots
    except Exception as e:
        print("❌ Error fetching spots:", e)
        return []


def mark_spot_reserved(spot_id):
    #Updates parking spot status
    try:
        result = spots_collection.update_one({"spot_id": spot_id}, {"$set": {"status": "reserved"}})
        if result.modified_count:
            print(f"✅ Spot {spot_id} marked as reserved.")
        else:
            print(f"⚠️ Spot {spot_id} was not updated (maybe already reserved?).")
    except Exception as e:
        print("❌ Error marking spot reserved:", e)