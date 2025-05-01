import unittest
from unittest.mock import patch, MagicMock

class TestReservationFunctions(unittest.TestCase):

    @patch("Backend.Database.connect_mongo.get_mongo_collections")
    def test_list_reservations(self, mock_get_mongo):
        mock_reservations = MagicMock()
        mock_reservations.find.return_value = [{"parking_spot": "A1", "reservation_time": "2025-05-01", "status": "active", "_id": "12345"}]
        mock_get_mongo.return_value = (None, mock_reservations)

        result = list_reservations()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["parking_spot"], "A1")

    @patch("Backend.Database.connect_mongo.get_mongo_collections")
    def test_cancel_reservation_by_id(self, mock_get_mongo):
        mock_reservations = MagicMock()
        mock_reservations.find_one.return_value = {"_id": ObjectId("12345"), "parking_spot": "A1"}
        mock_get_mongo.return_value = (None, mock_reservations)

        with patch("Backend.Database.connect_mongo.spots_collection.update_one") as mock_spot_update:
            cancel_reservation_by_id("12345")
            mock_reservations.update_one.assert_called_once()
            mock_spot_update.assert_called_once()

if __name__ == "__main__":
    unittest.main()
