# dataviewer_ui.py (Python)
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DataViewer(object):
    def setupUi(self, DataViewer):
        DataViewer.setObjectName("DataViewer")
        DataViewer.resize(800, 600)
        self.gridLayout = QtWidgets.QGridLayout(DataViewer)
        self.gridLayout.setObjectName("gridLayout")
        self.table_widget = QtWidgets.QTableWidget(parent=DataViewer)
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.gridLayout.addWidget(self.table_widget, 0, 0, 1, 1)
        self.retranslateUi(DataViewer)
        QtCore.QMetaObject.connectSlotsByName(DataViewer)

    def retranslateUi(self, DataViewer):
        _translate = QtCore.QCoreApplication.translate
        DataViewer.setWindowTitle(_translate("DataViewer", "Trình xem dữ liệu"))