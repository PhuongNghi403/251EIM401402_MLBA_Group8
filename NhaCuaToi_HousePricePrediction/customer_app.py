from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from UI.customer_home_ui import Ui_CustomerHome
from SharedLogic import PredictionLogicMixin

class CustomerWindow(QMainWindow, Ui_CustomerHome, PredictionLogicMixin):
    def __init__(self, username: str = "customer"):
        super().__init__()
        self.ui = Ui_CustomerHome()
        self.ui.setupUi(self)
        PredictionLogicMixin.__init__(self)
        self.current_user = username
        self.current_role = "customer"

        # Set icon cho btn_logout bằng QStyle
        style = self.style()
        self.ui.btn_logout.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_TitleBarCloseButton))

        # Kết nối nút
        self.ui.btn_predict.clicked.connect(self.slot_predict)
        self.ui.btn_export_report.clicked.connect(self.slot_export_report)
        self.ui.btn_logout.clicked.connect(self._handle_logout)

        # Lịch sử
        self.ui.btn_delete_history.clicked.connect(self.slot_delete_history)
        self.ui.btn_clear_history.clicked.connect(self.slot_clear_history)
        self.ui.btn_export_history.clicked.connect(self.slot_export_history)

        # Áp dụng theme và chuẩn hóa bảng
        self._apply_theme(getattr(self, "_theme_mode", "dark"))
        self.ui.table_history.setColumnCount(4)
        self.ui.table_history.setHorizontalHeaderLabels(["Time", "Input Summary", "Predicted Price", "Model"])

    def _error(self, msg: str):
        QMessageBox.critical(self, "Error", msg)

    def _handle_logout(self):
        from login_app import LoginWindow
        self.close()
        self._login = LoginWindow()
        self._login.show()