import unittest
from unittest.mock import patch
from Frontend.login import LoginWindow
from PyQt5.QtWidgets import QMessageBox

class TestLoginWindow(unittest.TestCase):
    @patch("Backend.Authorization.auth.validate_login")
    def test_handle_login_success(self, mock_validate):
        mock_validate.return_value = True
        window = LoginWindow()
        window.username_input.setText("test_user")
        window.password_input.setText("test_password")

        with patch.object(QMessageBox, "information") as mock_info:
            window.handle_login()

        mock_info.assert_called_with(window, "Login", "Welcome, test_user!")

    @patch("Backend.Authorization.auth.validate_login")
    def test_handle_login_failed(self, mock_validate):
        mock_validate.return_value = False
        window = LoginWindow()
        window.username_input.setText("test_user")
        window.password_input.setText("wrong_password")

        with patch.object(QMessageBox, "warning") as mock_warning:
            window.handle_login()

        mock_warning.assert_called_with(window, "Login Failed", "Invalid username or password.")

if __name__ == "__main__":
    unittest.main()
