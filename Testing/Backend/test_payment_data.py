import pytest
import mongomock
from datetime import datetime, timedelta
from bson import ObjectId

from Backend.Logic.payment_data import get_user_payment_history

@pytest.fixture
def mock_mongo(monkeypatch):
    client = mongomock.MongoClient()
    db = client["parking_db"]
    payments = db["payments"]
    reservations = db["reservations"]

    monkeypatch.setattr("Backend.Logic.payment_data.MongoClient", lambda *a, **kw: client)
    return payments, reservations

def test_get_user_payment_history_with_reservation(mock_mongo):
    payments, reservations = mock_mongo

    res_id = reservations.insert_one({
        "_id": ObjectId(),
        "parking_spot": "A1",
        "reservation_time": datetime(2024, 1, 1, 14, 30)
    }).inserted_id

    payments.insert_one({
        "user_id": "testuser",
        "amount": 5.0,
        "method": "credit_card",
        "status": "completed",
        "reservation_id": res_id,
        "date": datetime(2024, 1, 1, 13, 45)
    })

    history = get_user_payment_history("testuser")
    assert "testuser" not in history  # user_id is not printed
    assert "A1" in history
    assert "2024-01-01 14:30" in history
    assert "€5.0" in history
    assert "credit_card" in history
    assert "completed" in history

def test_get_user_payment_history_no_reservation(mock_mongo):
    payments, reservations = mock_mongo

    payments.insert_one({
        "user_id": "nores_user",
        "amount": 3.0,
        "method": "debit_card",
        "status": "completed",
        "date": datetime(2024, 3, 15, 10, 0)
    })

    history = get_user_payment_history("nores_user")
    assert "Reservation: - at -" in history
    assert "debit_card" in history

def test_get_user_payment_history_empty(mock_mongo):
    history = get_user_payment_history("unknown_user")
    assert history == "No payments found."
