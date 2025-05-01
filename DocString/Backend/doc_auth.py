"""
Handles user authentication.

Connects to a MongoDB collection and provides two functions:
- `register_user` for adding new users with hashed passwords.
- `validate_login` for verifying login credentials.

Dependencies:
    - pymongo for database operations
    - bcrypt for password hashing and verification
    - certifi for trusted SSL certificates

MongoDB Collection:
    Database: user_auth
    Collection: users
"""

import bcrypt
import certifi
from pymongo import MongoClient

# MongoDB connection setup
uri = (
    "mongodb+srv://Skullgame300:Skullgame300"
    "@parking.v4glm.mongodb.net/user_auth"
    "?retryWrites=true&w=majority&appName=Parking"
)
client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())
db = client["user_auth"]
users = db["users"]

def register_user(username: str, password: str):
    """
    Registers new user and stores in the database.

    Args:
        username (str): Username
        password (str): Password.

    Returns:
        tuple: (bool, str)

    Fails if:
        - The username or password is empty.
        - The username already exists.
    """
    if not username or not password:
        return False, "Not empty!"
    if users.find_one({"username": username}):
        return False, "Username already exists!"
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users.insert_one({"username": username, "password": hashed})
    return True, "Registration successful!"

def validate_login(username: str, password: str):
    """
    Validateslogin credentials.

    Args:
        username (str): Username
        password (str): Password

    Returns:
        bool:
    """
    user = users.find_one({"username": username})
    return bool(user and bcrypt.checkpw(password.encode("utf-8"), user["password"]))
