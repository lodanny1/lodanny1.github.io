from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from Frontend.register_window import RegisterWindow
from Frontend.dashboard import DashboardWindow
from Backend.Authorization.auth import validate_login

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        """
        Initializes login window.
        """
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setGeometry(150, 150, 300, 180)
        self.init_ui()

    def init_ui(self):
        """
        Sets up UI.
        """
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)

        register_btn = QPushButton("Create Account")
        register_btn.clicked.connect(self.open_register)
        layout.addWidget(register_btn)

        self.setLayout(layout)

    def handle_login(self):
        """
        Handles the login  and opens Dashboard window.
        """
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if validate_login(username, password):
            QMessageBox.information(self, "Login", f"Welcome, {username}!")
            self.dashboard = DashboardWindow(username)
            self.dashboard.show()
            self.close()  # Close the LoginWindow after successful login
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def open_register(self):
        """
        Opens registration window.
        """
        self.reg_window = RegisterWindow()
        self.reg_window.show()
