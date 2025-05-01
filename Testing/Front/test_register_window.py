import pytest
from PyQt5.QtWidgets import QApplication, QLineEdit
from Frontend.register_window import RegisterWindow

# Mocked backend function
def fake_register_user(username, password):
    if username == "exists":
        return False, "Username already exists!"
    return True, "Registration successful!"

@pytest.fixture(scope="module")
def app():
    return QApplication([])

def test_register_window_initial_state(app):
    window = RegisterWindow()
    assert window.windowTitle() == "Create Account"
    assert isinstance(window.username_input, QLineEdit)
    assert isinstance(window.password_input, QLineEdit)
    assert window.password_input.echoMode() == QLineEdit.Password

def test_handle_register_success(monkeypatch, qtbot, app):
    monkeypatch.setattr(
        "Frontend.register_window.register_user",
        fake_register_user
    )

    window = RegisterWindow()
    qtbot.addWidget(window)

    window.username_input.setText("new_user")
    window.password_input.setText("securepass")

    qtbot.mouseClick(window.findChild(QPushButton, "Register"), qtbot.LeftButton)
    assert not window.isVisible()  # Should close on success

def test_handle_register_failure(monkeypatch, qtbot, app):
    monkeypatch.setattr(
        "Frontend.register_window.register_user",
        fake_register_user
    )

    window = RegisterWindow()
    qtbot.addWidget(window)

    window.username_input.setText("exists")
    window.password_input.setText("password")

    qtbot.mouseClick(window.findChild(QPushButton, "Register"), qtbot.LeftButton)
    assert window.isVisible()  # Should stay open on failure
