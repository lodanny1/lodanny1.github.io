import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QMessageBox
from Backend.Logic.delete_reservation import cancel_reservation_by_id
from Frontend.dashboard import DashboardWindow

class TestDashboardWindow(unittest.TestCase):
    @patch("Backend.Logic.dashboard_logic.get_user_reservation")
    def test_refresh_dashboard_with_reservation(self, mock_get_reservation):
        mock_get_reservation.return_value = {"parking_spot": "A1", "reservation_time": "2025-05-01", "end_time": "2025-05-02"}

        window = DashboardWindow("test_user")
        window.refresh_dashboard()

        self.assertEqual(window.reservation_label.text(), "Current Reservation:\nSpot: A1 | Start: 2025-05-01 00:00 | Ends: 2025-05-02 00:00")

    @patch("Backend.Logic.dashboard_logic.get_user_reservation")
    def test_refresh_dashboard_no_reservation(self, mock_get_reservation):
        mock_get_reservation.return_value = None

        window = DashboardWindow("test_user")
        window.refresh_dashboard()

        self.assertEqual(window.reservation_label.text(), "Current Reservation:\nNo active reservation.")

    @patch("Backend.Logic.delete_reservation.cancel_reservation_by_id")
    def test_cancel_reservation(self, mock_cancel):
        mock_cancel.return_value = None

        window = DashboardWindow("test_user")
        window.current_reservation = {"_id": "12345", "parking_spot": "A1"}
        
        with patch.object(QMessageBox, "question", return_value=QMessageBox.Yes):
            window.cancel_reservation()

        mock_cancel.assert_called_with("12345")
        self.assertIn("Your reservation was cancelled.", window.reservation_label.text())

if __name__ == "__main__":
    unittest.main()
