import sys
from PyQt6.QtWidgets import QApplication
from login_app import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())