"""
Displays a user's payment history.

Retrieves and displays user's past payment records.

Classes:
    PaymentHistoryWindow: Shows the user's payment history.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from Backend.Logic.payment_data import get_user_payment_history

class PaymentHistoryWindow(QWidget):
    """
    Displays the payment history for user.

    Attributes:
        username (str): Username
    """

    def __init__(self, username, parent=None):
        """
        Initializes PaymentHistoryWindow.

        Args:
            username (str): Username
            parent (QWidget, optional): Parent widget
        """
        super().__init__(parent)
        self.username = username
        self.setWindowTitle("Payment History")
        self.setGeometry(200, 200, 600, 400)

        self.init_ui()

    def init_ui(self):
        """
        Sets up the user interface
        """
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Payment History for {self.username}"))

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        self.setLayout(layout)
        self.load_payments()

    def load_payments(self):
        """
        Loads user's payment history and displays.
        """
        try:
            text = get_user_payment_history(self.username)
            self.text_area.setText(text)
        except Exception as e:
            self.text_area.setText(f"Error loading payment history:\n{e}")
