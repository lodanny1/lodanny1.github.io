import mongomock
import pytest
from unittest.mock import patch
from datetime import datetime
from pymongo.collection import Collection

from Backend.Logic.insert_payment import simulate_payment, insert_payment

@pytest.fixture
def mock_payments_collection(monkeypatch):
    mock_client = mongomock.MongoClient()
    payments = mock_client["test_db"]["payments"]
    monkeypatch.setattr("Backend.Logic.insert_payment.payments_collection", payments)
    return payments

def test_simulate_payment_returns_completed_or_failed():
    with patch("random.random", return_value=0.05): 
        assert simulate_payment("credit_card") == "completed"
        assert simulate_payment("debit_card") == "completed"

    with patch("random.random", return_value=0.95): 
        assert simulate_payment("credit_card") == "failed"
        assert simulate_payment("debit_card") == "failed"

    assert simulate_payment("bitcoin") == "failed"

def test_insert_payment_success(mock_payments_collection):
    with patch("random.random", return_value=0.01): 
        payment_id = insert_payment("testuser", 10.0, "credit_card")
        assert payment_id is not None
        assert mock_payments_collection.count_documents({}) == 1

def test_insert_payment_failure(mock_payments_collection):
    with patch("random.random", return_value=0.99): 
        payment_id = insert_payment("testuser", 10.0, "credit_card")
        assert payment_id is None
        assert mock_payments_collection.count_documents({}) == 1 

def test_insert_payment_manual_status(mock_payments_collection):
    payment_id = insert_payment("manualuser", 15.5, "credit_card", status="completed")
    assert payment_id is not None
    doc = mock_payments_collection.find_one({"user_id": "manualuser"})
    assert doc["status"] == "completed"
