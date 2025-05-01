import pytest
import mongomock
from datetime import datetime, timedelta
from unittest.mock import patch

from Backend.Logic.make_reservation_with_payment import make_reservation_with_payment

@pytest.fixture
def mock_collections(monkeypatch):
    client = mongomock.MongoClient()
    db = client["test_db"]
    monkeypatch.setattr("Backend.Logic.make_reservation_with_payment.reservations_collection", db["reservations"])
    monkeypatch.setattr("Backend.Logic.make_reservation_with_payment.payments_collection", db["payments"])
    return db

def test_make_reservation_success(monkeypatch, mock_collections):
    # Patch dependencies
    monkeypatch.setattr("Backend.Logic.make_reservation_with_payment.insert_payment", lambda *a, **kw: "pay123")
    monkeypatch.setattr("Backend.Logic.make_reservation_with_payment.update_expired_reservations", lambda: None)
    monkeypatch.setattr("Backend.Logic.make_reservation_with_payment.calculate_price", lambda mins: 5.0)

    now = datetime.now()

    res_id = make_reservation_with_payment(
        parking_spot="A1",
        reservation_time=now,
        duration_minutes=30,
        amount=0,  # ignored in function anyway
        method="credit_card",
        user_id="test_user"
    )

    assert res_id is not None
    doc = mock_collections["reservations"].find_one({"_id": res_id})
    assert doc["parking_spot"] == "A1"
    assert doc["user_id"] == "test_user"
    assert doc["status"] == "active"
    assert doc["payment_id"] == "pay123"

def test_make_reservation_conflict(monkeypatch, mock_collections):
    monkeypatch.setattr("Backend.Logic.make_reservation_with_payment.insert_payment", lambda *a, **kw: "pay999")
    monkeypatch.setattr("Backend.Logic.make_reservation_with_payment.update_expired_reservations", lambda: None)
    monkeypatch.setattr("Backend.Logic.make_reservation_with_payment.calculate_price", lambda mins: 2.0)

    now = datetime.now()
    conflict_res = {
        "user_id": "another",
        "parking_spot": "B2",
        "reservation_time": now - timedelta(minutes=10),
        "end_time": now + timedelta(minutes=30),
        "status": "active",
        "payment_id": "payABC",
        "created_at": now
    }
    mock_collections["reservations"].insert_one(conflict_res)

    res_id = make_reservation_with_payment(
        parking_spot="B2",
        reservation_time=now,
        duration_minutes=30,
        amount=0,
        method="credit_card",
        user_id="test_user"
    )

    assert res_id is None
