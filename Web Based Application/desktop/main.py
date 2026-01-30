import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from ui import MainWindow
from login_dialog import LoginDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set global stylesheet for deeper customization
    app.setStyleSheet("""
        QLineEdit { padding: 6px; border: 1px solid #ccc; border-radius: 4px; }
        QLabel { font-family: Segoe UI, sans-serif; }
        QListWidget { border: 1px solid #ddd; background: #fff; }
        QPushButton:hover { background-color: #1d4ed8; }
    """)

    # Show Login Dialog First
    login = LoginDialog()
    if login.exec_() == LoginDialog.Accepted:
        token = login.get_token()
        if token:
            window = MainWindow(token)
            window.show()
            sys.exit(app.exec_())
        else:
            QMessageBox.critical(None, "Error", "Login successful but no token received.")
            sys.exit(1)
    else:
        sys.exit(0)