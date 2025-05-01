from pymongo import MongoClient
import certifi  # Required for SSL certificate validation

def get_mongo_collections():
    uri = "mongodb+srv://flavienmaameri57:DCU9o2Vg0K8PvjnG@parking.v4glm.mongodb.net/?retryWrites=true&w=majority&appName=Parking"

    # Use certifi's CA bundle to fix the SSL error
    client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())
    db = client["parking_db"]

    payments = db["payments"]
    reservations = db["reservations"]

    return payments, reservations