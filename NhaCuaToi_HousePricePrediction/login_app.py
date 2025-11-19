from PyQt6.QtWidgets import QWidget, QMessageBox
from UI.login_ui import Ui_Login

class LoginWindow(QWidget, Ui_Login):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.ui.btn_login.clicked.connect(self._on_login)
        if hasattr(self.ui, "combo_role"):
            try:
                self.ui.combo_role.currentTextChanged.connect(self._on_role_changed)
                self._on_role_changed(self.ui.combo_role.currentText())
            except Exception:
                pass

    def _on_login(self):
        username = self.ui.txt_username.text().strip()
        password = self.ui.txt_password.text().strip()
        role = (self.ui.combo_role.currentText().strip().lower()
                if hasattr(self.ui, "combo_role") else "customer")

        if role == "admin":
            if username == "admin" and password == "admin":
                try:
                    from ml_studio_app import MainWindow
                    self._main = MainWindow()
                    self._main.current_user = username
                    self._main.current_role = "admin"
                    try:
                        self._main.apply_role_permissions()
                    except Exception:
                        pass
                    self._main.show()
                    self.close()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Cannot open Admin: {e}")
            else:
                QMessageBox.warning(self, "Login failed", "Sai tài khoản/mật khẩu admin (admin/admin).")
        else:  # customer
            if username == "customer" and password == "123":
                try:
                    from customer_app import CustomerWindow
                    self._cust = CustomerWindow(username=username)
                    self._cust.show()
                    self.close()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Cannot open Customer: {e}")
            else:
                QMessageBox.warning(self, "Login failed", "Sai tài khoản/mật khẩu customer (customer/123).")

    def _on_role_changed(self, text: str):
        role = (text or "").strip().lower()
        if role == "admin":
            self.ui.txt_username.setText("admin")
            self.ui.txt_password.setText("admin")
        else:
            self.ui.txt_username.setText("customer")
            self.ui.txt_password.setText("123")