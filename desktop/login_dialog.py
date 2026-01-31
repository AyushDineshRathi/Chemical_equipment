from PyQt5.QtWidgets import (
    QDialog, QLineEdit, QVBoxLayout, QPushButton, QLabel, QMessageBox, QFrame, QHBoxLayout
)
from PyQt5.QtCore import Qt
from api import login, register

LOGIN_STYLESHEET = """
QDialog {
    background-color: #f8fafc;
}
QLineEdit {
    padding: 8px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 14px;
}
QLineEdit:focus {
    border: 1px solid #3b82f6;
}
QPushButton#ActionBtn {
    background-color: #3b82f6;
    color: white;
    padding: 8px;
    border-radius: 6px;
    font-weight: bold;
    border: none;
}
QPushButton#ActionBtn:hover {
    background-color: #2563eb;
}
QLabel#ToggleLink {
    color: #3b82f6;
    font-weight: bold;
    text-decoration: underline;
}
QLabel#ToggleLink:hover {
    color: #2563eb;
}
QFrame#Card {
    background-color: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
}
"""

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setFixedSize(360, 320)
        self.setStyleSheet(LOGIN_STYLESHEET)
        self.token = None
        self.is_login_mode = True
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Card Frame
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedSize(320, 260)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(15)
        card_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        self.title_label = QLabel("Welcome Back")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b;")
        self.title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title_label)
        
        # Inputs
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        card_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.password_input)

        # Action Button
        self.action_btn = QPushButton("Login")
        self.action_btn.setObjectName("ActionBtn")
        self.action_btn.setCursor(Qt.PointingHandCursor)
        self.action_btn.clicked.connect(self.handle_action)
        card_layout.addWidget(self.action_btn)

        # Toggle Mode
        toggle_layout = QHBoxLayout()
        toggle_layout.setAlignment(Qt.AlignCenter)
        
        self.msg_label = QLabel("Don't have an account?")
        self.msg_label.setStyleSheet("color: #64748b; font-size: 12px;")
        
        self.toggle_btn = QPushButton("Sign Up")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.setStyleSheet("""
            border: none; 
            background: transparent; 
            color: #3b82f6; 
            font-weight: bold; 
            font-size: 12px;
        """)
        self.toggle_btn.clicked.connect(self.toggle_mode)
        
        toggle_layout.addWidget(self.msg_label)
        toggle_layout.addWidget(self.toggle_btn)
        card_layout.addLayout(toggle_layout)
        
        main_layout.addWidget(card)

    def toggle_mode(self):
        self.is_login_mode = not self.is_login_mode
        self.username_input.clear()
        self.password_input.clear()
        
        if self.is_login_mode:
            self.title_label.setText("Welcome Back")
            self.action_btn.setText("Login")
            self.msg_label.setText("Don't have an account?")
            self.toggle_btn.setText("Sign Up")
        else:
            self.title_label.setText("Create Account")
            self.action_btn.setText("Sign Up")
            self.msg_label.setText("Already have an account?")
            self.toggle_btn.setText("Login")

    def handle_action(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        try:
            if self.is_login_mode:
                self.token = login(username, password)
                self.accept()
            else:
                register(username, password)
                QMessageBox.information(self, "Success", "Registration successful! Please login.")
                self.toggle_mode()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def get_token(self):
        return self.token
