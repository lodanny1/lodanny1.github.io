import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from Backend.Logic.check_availability import is_spot_available, update_expired_reservations, run_auto_update


class TestReservationLogic(unittest.TestCase):

    @patch('Backend.Logic.check_availability.reservations_collection.find')
    def test_is_spot_available(self, mock_find):
        mock_find.return_value = []
        parking_spot = 'A1'
        start_time = datetime(2025, 4, 30, 14, 0)
        duration_minutes = 30

        result = is_spot_available(parking_spot, start_time, duration_minutes)
        self.assertTrue(result)  

        mock_find.return_value = [{'reservation_time': start_time - timedelta(minutes=10), 'end_time': start_time + timedelta(minutes=10), 'status': 'active'}]  # Overlapping reservation

        result = is_spot_available(parking_spot, start_time, duration_minutes)
        self.assertFalse(result) 

    @patch('Backend.Logic.check_availability.reservations_collection.update_many')
    def test_update_expired_reservations(self, mock_update_many):
        mock_update_many.return_value.modified_count = 3 

        with patch('builtins.print') as mocked_print:
            update_expired_reservations()
            mocked_print.assert_called_with("3 expired reservation(s).")  
    @patch('Backend.Logic.check_availability.update_expired_reservations')
    @patch('time.sleep')
    def test_run_auto_update(self, mock_sleep, mock_update_expired_reservations):

        mock_update_expired_reservations.return_value = None  
        run_auto_update(interval_seconds=1)
        mock_update_expired_reservations.assert_called()  
        mock_sleep.assert_called_with(1)  
if __name__ == '__main__':
    unittest.main()
