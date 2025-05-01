"""
User registration window.

Classes:
    RegisterWindow: Provides registration form.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from Backend.Authorization.auth import register_user

class RegisterWindow(QWidget):
    """
    Registration form window that allows new users to create an account.

    Attributes:
        username_input (QLineEdit): new username
        password_input (QLineEdit): new password
    """

    def __init__(self, parent=None):
        """
        Initializes the RegisterWindow.

        Args:
            parent (QWidget, optional): The parent widget
        """
        super().__init__(parent)
        self.setWindowTitle("Create Account")
        self.setGeometry(200, 200, 300, 200)
        self.init_ui()

    def init_ui(self):
        """
        Sets up the registration form UI
        """
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.handle_register)
        layout.addWidget(register_btn)

        self.setLayout(layout)

    def handle_register(self):
        """
        Handles the registration logic.

        Retrieves username and password, then calls register_user.
        """
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        success, message = register_user(username, password)
        if success:
            QMessageBox.information(self, "Success", message)
            self.close()
        else:
            QMessageBox.warning(self, "Error", message)
