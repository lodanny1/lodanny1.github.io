import pytest
import mongomock
from datetime import datetime, timedelta

from Backend.Logic.check_availability import update_expired_reservations

@pytest.fixture
def mock_collections(monkeypatch):
    client = mongomock.MongoClient()
    db = client["parking_db"]

    monkeypatch.setattr("Backend.Logic.check_availability.reservations_collection", db["reservations"])
    monkeypatch.setattr("Backend.Logic.check_availability.spots_collection", db["parking_spots"])

    return db["reservations"], db["parking_spots"]

def test_update_expired_reservations(mock_collections, capsys):
    reservations, spots = mock_collections
    now = datetime.now()

    reservations.insert_one({
        "user_id": "user1",
        "parking_spot": "A1",
        "end_time": now - timedelta(minutes=1),
        "status": "active"
    })

    reservations.insert_one({
        "user_id": "user2",
        "parking_spot": "A2",
        "end_time": now + timedelta(minutes=30),
        "status": "active"
    })

    spots.insert_many([
        {"spot_id": "A1", "status": "reserved"},
        {"spot_id": "A2", "status": "reserved"},
    ])

    update_expired_reservations()

    expired = reservations.find_one({"parking_spot": "A1"})
    assert expired["status"] == "expired"

    still_active = reservations.find_one({"parking_spot": "A2"})
    assert still_active["status"] == "active"

    spot = spots.find_one({"spot_id": "A1"})
    assert spot["status"] == "available"

    spot = spots.find_one({"spot_id": "A2"})
    assert spot["status"] == "reserved"

    captured = capsys.readouterr()
    assert "Expired reservations updated: 1" in captured.out
    assert "Spot statuses updated to 'available': 1" in captured.out
