from PyQt5.QtWidgets import QInputDialog, QMessageBox
from datetime import datetime
from Backend.Logic.make_reservation_with_payment import make_reservation_with_payment  # adjust path

def reserve_spot(self):
    spot, ok1 = QInputDialog.getText(self, "Reserve Spot", "Enter parking spot (e.g. A1):")
    if not ok1 or not spot:
        return

    duration, ok2 = QInputDialog.getInt(self, "Duration", "Duration (minutes):", value=30)
    if not ok2 or duration <= 0:
        return

    method, ok3 = QInputDialog.getItem(self, "Payment Method", "Choose:", ["credit_card", "debit_card"], 0, False)
    if not ok3 or not method:
        return

    now = datetime.now()
    amount = 0

    reservation_id = make_reservation_with_payment(
        parking_spot=spot,
        reservation_time=now,
        duration_minutes=duration,
        amount=amount,
        method=method
    )

    if reservation_id:
        QMessageBox.information(self, "Reservation Success", f"Reservation confirmed!\nID: {reservation_id}")
        self.refresh_dashboard()
    else:
        QMessageBox.warning(self, "Failed", "Reservation failed.")
