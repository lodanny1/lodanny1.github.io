from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
)
from datetime import datetime

from Frontend.payment_history_window import PaymentHistoryWindow
from Frontend.reserve_map import ReserveMapWindow
from Backend.Logic.dashboard_logic import get_user_reservation
from Backend.Logic.delete_reservation import cancel_reservation_by_id

class DashboardWindow(QWidget):
    def __init__(self, username, parent=None):
        """
        Initializes Dashboard with the username.
        """
        super().__init__(parent)
        self.username = username
        self.setWindowTitle(f"Dashboard - {username}")
        self.setGeometry(150, 150, 400, 350)
        self.init_ui()

    def init_ui(self):
        """
        Initializes UI and sets up buttons for different actions.
        """
        layout = QVBoxLayout()

        # Show current reservation
        self.current_reservation = get_user_reservation(self.username)
        res_text = self.format_reservation_text(self.current_reservation)
        self.reservation_label = QLabel(f"Current Reservation:\n{res_text}")
        layout.addWidget(self.reservation_label)

        # Reserve spot
        reserve_btn = QPushButton("Reserve Parking Spot")
        reserve_btn.clicked.connect(self.reserve_spot)
        layout.addWidget(reserve_btn)

        # Cancel reservation
        cancel_btn = QPushButton("Cancel Current Reservation")
        cancel_btn.clicked.connect(self.cancel_reservation)
        layout.addWidget(cancel_btn)

        # Payments
        payments_btn = QPushButton("View Payment History")
        payments_btn.clicked.connect(self.view_payments)
        layout.addWidget(payments_btn)

        # Logout
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

        self.setLayout(layout)

    def format_reservation_text(self, reservation):
        """
        Formats reservation text and display details of the current reservation.

        Args:
            reservation (dict): Reservation details to display.

        Returns:
            str: Formatts reservation details
        """
        if reservation:
            return (
                f"Spot: {reservation.get('parking_spot')} | "
                f"Start: {reservation.get('reservation_time').strftime('%Y-%m-%d %H:%M')} | "
                f"Ends: {reservation.get('end_time').strftime('%Y-%m-%d %H:%M')}"
            )
        else:
            return "No active reservation."

    def refresh_dashboard(self):
        """
        Refreshes dashboard with updated reservation data.
        """
        self.current_reservation = get_user_reservation(self.username)
        res_text = self.format_reservation_text(self.current_reservation)
        self.reservation_label.setText(f"Current Reservation:\n{res_text}")

    def reserve_spot(self):
        """
        Opens map for reserving a parking spot.
        """
        self.close()  # Close the Dashboard window
        self.reserve_map = ReserveMapWindow(username=self.username)
        self.reserve_map.show()

    def cancel_reservation(self):
        """
        Cancels current reservation if active.
        """
        if not self.current_reservation:
            QMessageBox.information(self, "No Reservation", "There is no active reservation to cancel.")
            return

        confirm = QMessageBox.question(
            self, "Cancel Reservation",
            "Are you sure you want to cancel your current reservation?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            cancel_reservation_by_id(self.current_reservation['_id'])
            self.refresh_dashboard()
            QMessageBox.information(self, "Cancelled", "Your reservation was cancelled.")

    def view_payments(self):
        """
        Opens the PaymentHistoryWindow to view the user's payment history.
        """
        self.payment_window = PaymentHistoryWindow(username=self.username)
        self.payment_window.show()

    def logout(self):
        """
        Logs out the user and closes the dashboard.
        """
        QMessageBox.information(self, "Logout", "Logging out...")
        self.close()
