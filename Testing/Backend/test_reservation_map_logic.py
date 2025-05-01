import pytest
import mongomock

from Backend.Logic.reservation_map_logic import fetch_spots, mark_spot_reserved

@pytest.fixture
def mock_spots_collection(monkeypatch):
    client = mongomock.MongoClient()
    db = client["parking_db"]
    collection = db["parking_spots"]

    monkeypatch.setattr("Backend.Logic.reservation_map_logic.spots_collection", collection)
    return collection

def test_fetch_spots_sorted(mock_spots_collection):
    mock_spots_collection.insert_many([
        {"spot_id": "B2", "status": "available", "lot_name": "LotB"},
        {"spot_id": "A1", "status": "reserved", "lot_name": "LotA"},
        {"spot_id": "A3", "status": "available", "lot_name": "LotA"},
    ])

    result = fetch_spots()
    assert isinstance(result, list)
    assert result[0]["spot_id"] == "A1"
    assert result[1]["spot_id"] == "A3"
    assert result[2]["spot_id"] == "B2"

def test_mark_spot_reserved_success(mock_spots_collection, capsys):
    mock_spots_collection.insert_one({"spot_id": "A1", "status": "available"})
    mark_spot_reserved("A1")

    updated = mock_spots_collection.find_one({"spot_id": "A1"})
    assert updated["status"] == "reserved"

    captured = capsys.readouterr()
    assert "✅ Spot A1 marked as reserved." in captured.out

def test_mark_spot_reserved_no_change(mock_spots_collection, capsys):
    mark_spot_reserved("Z9") #edge case
    captured = capsys.readouterr()
    assert "⚠️ Spot Z9 was not updated" in captured.out
