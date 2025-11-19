from PyQt6 import QtCore, QtWidgets, QtGui
import os

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(400, 240)
        self.verticalLayout_root = QtWidgets.QVBoxLayout(Login)
        self.verticalLayout_root.setObjectName("verticalLayout_root")
        self.vbox_center = QtWidgets.QVBoxLayout()
        self.vbox_center.setObjectName("vbox_center")
        self.lbl_title = QtWidgets.QLabel(parent=Login)
        self.lbl_title.setObjectName("lbl_title")
        self.lbl_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.vbox_center.addWidget(self.lbl_title)

        self.lbl_logo = QtWidgets.QLabel(parent=Login)
        self.lbl_logo.setObjectName("lbl_logo")
        self.lbl_logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.vbox_center.addWidget(self.lbl_logo)
        self.txt_username = QtWidgets.QLineEdit(parent=Login)
        self.txt_username.setObjectName("txt_username")
        self.vbox_center.addWidget(self.txt_username)
        self.txt_password = QtWidgets.QLineEdit(parent=Login)
        self.txt_password.setObjectName("txt_password")
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.vbox_center.addWidget(self.txt_password)

        # THÊM: label & combo vai trò
        self.lbl_role = QtWidgets.QLabel(parent=Login)
        self.lbl_role.setObjectName("lbl_role")
        self.vbox_center.addWidget(self.lbl_role)

        self.combo_role = QtWidgets.QComboBox(parent=Login)
        self.combo_role.setObjectName("combo_role")
        self.combo_role.addItems(["customer", "admin"])
        self.vbox_center.addWidget(self.combo_role)

        # Nút login
        self.btn_login = QtWidgets.QPushButton(parent=Login)
        self.btn_login.setObjectName("btn_login")
        self.vbox_center.addWidget(self.btn_login)
        self.verticalLayout_root.addLayout(self.vbox_center)
        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Login"))
        self.lbl_title.setText(_translate("Login", "HOUSE PRICE PREDICTION SYSTEM"))
        self.txt_username.setPlaceholderText(_translate("Login", "Username"))
        self.txt_password.setPlaceholderText(_translate("Login", "Password"))
        self.lbl_role.setText(_translate("Login", "Role"))
        # giữ nguyên thứ tự items đã thêm lúc setup
        self.btn_login.setText(_translate("Login", "Login"))

        Login.setStyleSheet(
            """
            QWidget {
                background: #ffffff;
                color: #2b2342;
                font-size: 14px;
            }
            QLabel#lbl_title {
                color: #4c0c24;
                font-weight: 700;
                font-size: 16px;
            }
            QLabel#lbl_logo {
                margin-top: 6px;
            }
            QLineEdit, QComboBox {
                background: #ffffff;
                color: #2b2342;
                border: 1px solid #d6b6f5;
                border-radius: 6px;
                padding: 6px 8px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #d491d3;
            }
            QPushButton {
                background: #4c0c24;
                color: #f8e1f4;
                border: 1px solid #4c0c24;
                border-radius: 6px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background: #f8e1f4;
                color: #4c0c24;
                border: 1px solid #4c0c24;
            }
            """
        )

        base_dir = os.path.dirname(os.path.dirname(__file__))
        img_path = os.path.join(base_dir, "LOGO.PNG")
        pix = QtGui.QPixmap(img_path)
        if pix and not pix.isNull():
            self.lbl_logo.setPixmap(pix.scaled(240, 140, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
        else:
            self.lbl_logo.setText("")