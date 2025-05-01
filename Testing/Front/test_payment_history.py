import pytest
from PyQt5.QtWidgets import QApplication, QTextEdit
from Frontend.payment_history_window import PaymentHistoryWindow

# Mock the backend function
def fake_get_user_payment_history(username):
    return f"Payment for {username}"

@pytest.fixture(scope="module")
def app():
    return QApplication([])

def test_window_initializes_with_username(monkeypatch, app):
    monkeypatch.setattr(
        "Frontend.payment_history_window.get_user_payment_history", 
        fake_get_user_payment_history
    )

    window = PaymentHistoryWindow("testuser")

    # Ensure title and geometry are set
    assert window.windowTitle() == "Payment History"
    assert window.username == "testuser"

    # Ensure QTextEdit contains expected mock text
    assert isinstance(window.text_area, QTextEdit)
    assert "Payment for testuser" in window.text_area.toPlainText()
