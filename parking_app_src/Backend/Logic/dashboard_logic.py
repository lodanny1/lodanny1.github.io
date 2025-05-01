from Backend.Database.connect_mongo import get_mongo_collections
from datetime import datetime

_, reservations_collection = get_mongo_collections()

def get_user_reservation(username):
    now = datetime.now()
    return reservations_collection.find_one({
        "user_id": username,
        "end_time": {"$gt": now},
        "status": {"$in": ["active", "upcoming"]}
    }, sort=[("reservation_time", -1)])


