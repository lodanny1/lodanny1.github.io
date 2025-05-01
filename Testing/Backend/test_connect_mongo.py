import pytest
from pymongo.collection import Collection
from Backend.Database.connect_mongo import get_mongo_collections  # adjust path if needed

def test_get_mongo_collections_returns_collections():
    payments, reservations = get_mongo_collections()
    assert isinstance(payments, Collection)
    assert isinstance(reservations, Collection)
    assert payments.name == "payments"
    assert reservations.name == "reservations"
