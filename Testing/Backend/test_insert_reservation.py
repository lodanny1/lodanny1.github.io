import pytest
import mongomock
from datetime import datetime, timedelta
from unittest.mock import patch

from Backend.Logic.insert_reservation import insert_reservation

@pytest.fixture
def mock_reservations_collection(monkeypatch):
    client = mongomock.MongoClient()
    mock_collection = client["test_db"]["reservations"]
    monkeypatch.setattr("Backend.Logic.insert_reservation.reservations_collection", mock_collection)
    return mock_collection

def test_insert_reservation_success(mock_reservations_collection, monkeypatch):
    monkeypatch.setattr("Backend.Logic.insert_reservation.is_spot_available", lambda *a, **kw: True)

    now = datetime.now()
    res_id = insert_reservation(
        user_id="test_user",
        parking_spot="A1",
        reservation_time=now,
        duration_minutes=60,
        payment_id="pay123"
    )

    assert res_id is not None
    doc = mock_reservations_collection.find_one({"_id": res_id})
    assert doc["user_id"] == "test_user"
    assert doc["parking_spot"] == "A1"
    assert doc["status"] == "active"

def test_insert_reservation_unavailable(mock_reservations_collection, monkeypatch):
    monkeypatch.setattr("Backend.Logic.insert_reservation.is_spot_available", lambda *a, **kw: False)

    now = datetime.now()
    res_id = insert_reservation(
        user_id="test_user",
        parking_spot="A1",
        reservation_time=now,
        duration_minutes=30
    )

    assert res_id is None
    assert mock_reservations_collection.count_documents({}) == 0
