import pytest
from PyQt5.QtWidgets import QApplication, QPushButton
from Frontend.reserve_map import ReserveMapWindow

# -------- MOCK FUNCTIONS -------- #

def mock_fetch_spots():
    return [
        {"spot_id": "A1", "status": "available", "lot_name": "LotA"},
        {"spot_id": "A2", "status": "reserved", "lot_name": "LotA"},
        {"spot_id": "B1", "status": "available", "lot_name": "LotB"},
    ]

def mock_make_reservation_with_payment(parking_spot, reservation_time, duration_minutes, amount, method, user_id):
    return "mock_reservation_id"

def mock_mark_spot_reserved(spot_id):
    print(f"Mock: Spot {spot_id} marked as reserved")

# -------- FIXTURES -------- #

@pytest.fixture(scope="module")
def app():
    return QApplication([])

@pytest.fixture
def window(monkeypatch, qtbot):
    monkeypatch.setattr("Frontend.reserve_map.fetch_spots", mock_fetch_spots)
    monkeypatch.setattr("Frontend.reserve_map.make_reservation_with_payment", mock_make_reservation_with_payment)
    monkeypatch.setattr("Frontend.reserve_map.mark_spot_reserved", mock_mark_spot_reserved)

    w = ReserveMapWindow("testuser")
    qtbot.addWidget(w)
    return w

# -------- TEST CASES -------- #

def test_window_title_and_username(window):
    assert window.windowTitle() == "Reserve a Parking Spot"
    assert window.username == "testuser"

def test_grid_renders_buttons(window):
    buttons = window.grid.parent().findChildren(QPushButton)
    button_texts = [btn.text() for btn in buttons if btn.text()]
    assert "A1" in button_texts
    assert "A2" in button_texts
    assert "B1" in button_texts

def test_spot_selection_enables_button(window, qtbot):
    button = [b for b in window.grid.parent().findChildren(QPushButton) if b.text() == "A1"][0]
    qtbot.mouseClick(button, qtbot.LeftButton)
    assert window.selected_spot == "A1"
    assert window.confirm_btn.isEnabled()

def test_confirm_reservation_valid_input(window, qtbot):
    # Simulate selection and valid form input
    window.select_spot("A1")
    window.duration_input.setText("30")
    qtbot.mouseClick(window.confirm_btn, qtbot.LeftButton)
    # Expect it to reach the mocked reservation logic and reset fields
    assert window.selected_spot is None
    assert not window.confirm_btn.isEnabled()
