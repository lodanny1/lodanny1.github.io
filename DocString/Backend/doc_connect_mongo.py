"""
MongoDB connects Parking App.

Providess function to connect to MongoDB

Dependencies:
    - pymongo: MongoDB
    - certifi: Provide SSL certificate
"""

from pymongo import MongoClient
import certifi  # ✅ Required for SSL certificate validation

def get_mongo_collections():
    """
    Establishes secure connection

    Returns:
        tuple: A tuple:
            - payments: Transaction records.
            - reservations: Parking reservation data.

    Raises:
        pymongo.errors.PyMongoError: If connection fails.
    """
    uri = (
        "mongodb+srv://flavienmaameri57:DCU9o2Vg0K8PvjnG@parking.v4glm.mongodb.net/"
        "?retryWrites=true&w=majority&appName=Parking"
    )

    # ✅ Use certifi's CA bundle to fix the SSL error
    client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())
    db = client["parking_db"]

    payments = db["payments"]
    reservations = db["reservations"]

    return payments, reservations
