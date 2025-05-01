import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from Frontend.login import LoginWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSULB Parking")
        self.setGeometry(100, 100, 300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to the CSULB"))

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login_clicked)
        layout.addWidget(login_btn)

        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout_clicked)
        layout.addWidget(logout_btn)

        self.setLayout(layout)

    def login_clicked(self):
        self.login_window = LoginWindow()
        self.login_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
