"""
ReserveMapWindow

Provides a visual map-like interface allowing users to:
- View available and reserved spots.
- Select a spot.
- Enter reservation duration.
- Choose payment method.
- Confirm reservation and marks spot as reserved.

Backend interactions:
- `fetch_spots()` gets current spot statuses.
- `make_reservation_with_payment()` to reserve and process payment.
- `mark_spot_reserved()` to update spot status.

Classes:
    ReserveMapWindow: Unit interface for selecting and confirming parking reservations.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QPushButton, QMessageBox, QLabel,
    QLineEdit, QComboBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from datetime import datetime

from Backend.Logic.reservation_map_logic import fetch_spots, mark_spot_reserved
from Backend.Logic.make_reservation_with_payment import make_reservation_with_payment

class ReserveMapWindow(QWidget):
    """
    Provides a interface for selecting and reserving parking spots.

    Attributes:
        username (str): User.
        selected_spot (str): Parking ID.
    """

    def __init__(self, username, parent=None):
        """
        Initializes reservation map window.

        Args:
            username (str): Username.
            parent (QWidget, optional): The parent widget
        """
        super().__init__(parent)
        self.username = username
        self.setWindowTitle("Reserve a Parking Spot")
        self.setGeometry(200, 200, 700, 600)
        self.setMinimumSize(600, 500)
        self.selected_spot = None
        self.init_ui()

    def init_ui(self):
        """
        Sets up all UI components, including the spot grid, input fields,
        and control buttons.
        """
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        self.setLayout(main_layout)

        self.title = QLabel(f"Select an available spot, {self.username}:")
        self.title.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)

        self.grid = QGridLayout()
        main_layout.addLayout(self.grid)

        control_layout = QVBoxLayout()
        self.selected_label = QLabel("Selected Spot: None")
        control_layout.addWidget(self.selected_label)

        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Enter duration in minutes")
        control_layout.addWidget(self.duration_input)

        self.method_box = QComboBox()
        self.method_box.addItems(["credit_card", "debit_card"])
        control_layout.addWidget(self.method_box)

        button_row = QHBoxLayout()
        self.confirm_btn = QPushButton("Confirm Reservation")
        self.confirm_btn.clicked.connect(self.confirm_reservation)
        self.confirm_btn.setEnabled(False)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.clear_selection)

        button_row.addWidget(self.confirm_btn)
        button_row.addWidget(cancel_btn)
        control_layout.addLayout(button_row)

        main_layout.addLayout(control_layout)
        self.load_spots()

    def load_spots(self):
        """
        Loads parking spot data and updates the grid.
        """
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

        spots = fetch_spots()
        row_map = {}
        row_counter = 0

        for spot in spots:
            lot = spot["lot_name"]
            if lot not in row_map:
                row_map[lot] = row_counter
                row_counter += 1

            row = row_map[lot]
            col = int(spot["spot_id"][1:]) - 1

            button = QPushButton(spot["spot_id"])
            button.setFixedSize(60, 40)

            if spot["status"] == "reserved":
                button.setStyleSheet("background-color: red;")
                button.setEnabled(False)
            else:
                button.setStyleSheet("background-color: green;")
                button.clicked.connect(lambda _, sid=spot["spot_id"]: self.select_spot(sid))

            self.grid.addWidget(button, row, col)

    def select_spot(self, spot_id):
        """
        Handles spot selection.

        Args:
            spot_id (str): Parking Spot ID.
        """
        self.selected_spot = spot_id
        self.selected_label.setText(f"Selected Spot: {spot_id}")
        self.confirm_btn.setEnabled(True)

    def clear_selection(self):
        """
        Clears the current spot selection.
        """
        self.selected_spot = None
        self.selected_label.setText("Selected Spot: None")
        self.confirm_btn.setEnabled(False)
        self.duration_input.clear()

    def confirm_reservation(self):
        """
        Validates input and confirms the reservation with payment.
        """
        if not self.selected_spot:
            QMessageBox.warning(self, "Missing Info", "No spot selected.")
            return

        try:
            duration = int(self.duration_input.text())
            if duration <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid Duration", "Please enter a valid number of minutes.")
            return

        method = self.method_box.currentText()
        now = datetime.now()

        reservation_id = make_reservation_with_payment(
            parking_spot=self.selected_spot,
            reservation_time=now,
            duration_minutes=duration,
            amount=0,
            method=method,
            user_id=self.username
        )

        if reservation_id:
            QMessageBox.information(self, "Success", f"Reserved {self.selected_spot}\nID: {reservation_id}")
            mark_spot_reserved(self.selected_spot)
            self.load_spots()
            self.clear_selection()
        else:
            QMessageBox.warning(self, "Failed", "Could not complete reservation.")
