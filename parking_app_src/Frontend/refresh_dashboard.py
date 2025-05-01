def refresh_dashboard(self):
    current = self.get_current_reservation()
    if current:
        res_text = (
            f"Spot: {current.get('parking_spot')} | "
            f"Start: {current.get('reservation_time').strftime('%Y-%m-%d %H:%M')} | "
            f"Ends: {current.get('end_time').strftime('%Y-%m-%d %H:%M')}"
        )
    else:
        res_text = "No active reservation."
    self.reservation_label.setText(f"Current Reservation:\n{res_text}")
