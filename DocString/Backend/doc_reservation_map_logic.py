"""
Utilities for the Parking App.

Connects to the parking_spots collection in MongoDB

Functions:
    fetch_spots: Retrieves parking spot records.
    mark_spot_reserved: Updates status of a given spot to reserved.
"""

from pymongo import MongoClient
import certifi

# MongoDB connection setup
uri = "mongodb+srv://Skullgame300:Skullgame300@parking.v4glm.mongodb.net/?retryWrites=true&w=majority&appName=Parking"
client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())
db = client["parking_db"]
spots_collection = db["parking_spots"]

def fetch_spots():
    """
    Fetches all parking spots from the MongoDB .

    Spots are returned as dictionaries containing:
        - spot_id
        - status (
        - lot_name

    Results sorted first by lot name, then by spot number.

    Returns:
        list: List of dictionaries representing parking spot data.
              Returns empty list if an error occurs.
    """
    try:
        spots = list(spots_collection.find({}, {"_id": 0, "spot_id": 1, "status": 1, "lot_name": 1}))
        spots.sort(key=lambda x: (x["lot_name"], int(x["spot_id"][1:])))
        return spots
    except Exception as e:
        print("❌ Error fetching spots:", e)
        return []

def mark_spot_reserved(spot_id):
    """
    Marks parking spot as reserved in database.

    Args:
        spot_id (str): ID of the spot.

    Effects:
        - Updates the status field.
        - Prints confirmation message if update is successful.

    Returns:
        None
    """
    try:
        result = spots_collection.update_one({"spot_id": spot_id}, {"$set": {"status": "reserved"}})
        if result.modified_count:
            print(f"✅ Spot {spot_id} marked as reserved.")
        else:
            print(f"⚠️ Spot {spot_id} was not updated (maybe already reserved?).")
    except Exception as e:
        print("❌ Error marking spot reserved:", e)
