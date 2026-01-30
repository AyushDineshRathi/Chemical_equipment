from PyQt5.QtWidgets import (
    QDialog, QLineEdit, QVBoxLayout, QPushButton, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt
from api import login

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Chemical Equipment Visualizer")
        self.setFixedSize(300, 200)
        self.token = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.on_login)
        self.login_btn.setStyleSheet("background-color: #2563eb; color: white; font-weight: bold; padding: 5px;")
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def on_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        try:
            token = login(username, password)
            self.token = token
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Login Failed", str(e))

    def get_token(self):
        return self.token
