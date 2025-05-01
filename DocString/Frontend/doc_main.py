"""
Main application window.

Initializes and displays the main menu.

Classes:
    MainWindow: Represents the main menu window with Login.

Usage:
    Run this script directly to launch the main menu window of the Parking App.
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from Frontend.login import LoginWindow

class MainWindow(QWidget):
    """
    Main window of the Parking App.
    """

    def __init__(self):
        """
        Initializes main window.
        """
        super().__init__()
        self.setWindowTitle("Parking App - Main Menu")
        self.setGeometry(100, 100, 300, 200)
        self.init_ui()

    def init_ui(self):
        """
        Sets up the UI components.
        """
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to the Parking App"))

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login_clicked)
        layout.addWidget(login_btn)

        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout_clicked)
        layout.addWidget(logout_btn)

        self.setLayout(layout)

    def login_clicked(self):
        """
        Opens the login window when clicked.
        """
        self.login_window = LoginWindow()
        self.login_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
