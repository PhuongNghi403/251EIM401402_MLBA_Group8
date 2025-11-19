from PyQt6 import QtCore, QtWidgets

class Ui_CustomerHome(object):
    def setupUi(self, CustomerHome):
        CustomerHome.setObjectName("CustomerHome")
        CustomerHome.resize(1280, 800)
        self.centralwidget = QtWidgets.QWidget(parent=CustomerHome)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_central = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_central.setObjectName("verticalLayout_central")
        self.widget_topbar = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget_topbar.setObjectName("widget_topbar")
        self.hbox_topbar = QtWidgets.QHBoxLayout(self.widget_topbar)
        self.hbox_topbar.setObjectName("hbox_topbar")
        self.hbox_topbar.setContentsMargins(12, 8, 12, 8)
        left_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hbox_topbar.addItem(left_spacer)
        self.lbl_header_title = QtWidgets.QLabel(parent=self.widget_topbar)
        self.lbl_header_title.setObjectName("lbl_header_title")
        self.lbl_header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_header_title.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred))
        self.hbox_topbar.addWidget(self.lbl_header_title)
        right_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hbox_topbar.addItem(right_spacer)
        self.btn_toggle_theme = QtWidgets.QPushButton(parent=self.widget_topbar)
        self.btn_toggle_theme.setObjectName("btn_toggle_theme")
        self.hbox_topbar.addWidget(self.btn_toggle_theme)
        self.btn_logout = QtWidgets.QPushButton(parent=self.widget_topbar)
        self.btn_logout.setObjectName("btn_logout")
        self.hbox_topbar.addWidget(self.btn_logout)
        self.verticalLayout_central.addWidget(self.widget_topbar)
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)
        self.verticalLayout_central.addWidget(self.tabWidget)
        self.tab_predict = QtWidgets.QWidget()
        self.tab_predict.setObjectName("tab_predict")
        self.vbox_predict = QtWidgets.QVBoxLayout(self.tab_predict)
        self.vbox_predict.setObjectName("vbox_predict")
        # Loại bỏ 2 khung trên, chỉ giữ House Input Form

        # Inline House Input Form group (replace popup button)
        self.group_house_inline = QtWidgets.QGroupBox(parent=self.tab_predict)
        self.group_house_inline.setObjectName("group_house_inline")
        self.vbox_house_inline = QtWidgets.QVBoxLayout(self.group_house_inline)
        self.vbox_house_inline.setObjectName("vbox_house_inline")
        # Container where the HouseInputForm widget will be embedded
        self.widget_house_inline_container = QtWidgets.QWidget(parent=self.group_house_inline)
        self.widget_house_inline_container.setObjectName("widget_house_inline_container")
        self.vbox_house_inline.addWidget(self.widget_house_inline_container)
        self.vbox_predict.addWidget(self.group_house_inline)
        self.group_price_chart = QtWidgets.QGroupBox(parent=self.tab_predict)
        self.group_price_chart.setObjectName("group_price_chart")
        self.vbox_price_chart = QtWidgets.QVBoxLayout(self.group_price_chart)
        self.vbox_price_chart.setObjectName("vbox_price_chart")
        self.hbox_price_charts = QtWidgets.QHBoxLayout()
        self.hbox_price_charts.setObjectName("hbox_price_charts")
        self.chart_view_price_trend = QtWidgets.QWidget(parent=self.group_price_chart)
        self.chart_view_price_trend.setObjectName("chart_view_price_trend")
        self.chart_view_price_breakdown = QtWidgets.QWidget(parent=self.group_price_chart)
        self.chart_view_price_breakdown.setObjectName("chart_view_price_breakdown")
        self.hbox_price_charts.addWidget(self.chart_view_price_trend)
        self.hbox_price_charts.addWidget(self.chart_view_price_breakdown)
        self.vbox_price_chart.addLayout(self.hbox_price_charts)
        self.vbox_predict.addWidget(self.group_price_chart)
        self.hbox_predict_exports = QtWidgets.QHBoxLayout()
        self.hbox_predict_exports.setObjectName("hbox_predict_exports")
        self.btn_export_csv = QtWidgets.QPushButton(parent=self.tab_predict)
        self.btn_export_csv.setObjectName("btn_export_csv")
        self.btn_export_pdf = QtWidgets.QPushButton(parent=self.tab_predict)
        self.btn_export_pdf.setObjectName("btn_export_pdf")
        self.hbox_predict_exports.addWidget(self.btn_export_csv)
        self.hbox_predict_exports.addWidget(self.btn_export_pdf)
        self.vbox_predict.addLayout(self.hbox_predict_exports)
        
        self.tabWidget.addTab(self.tab_predict, "Price Prediction")
        self.tab_history = QtWidgets.QWidget()
        self.tab_history.setObjectName("tab_history")
        self.vbox_history = QtWidgets.QVBoxLayout(self.tab_history)
        self.vbox_history.setObjectName("vbox_history")
        self.group_history_chart = QtWidgets.QGroupBox(parent=self.tab_history)
        self.group_history_chart.setObjectName("group_history_chart")
        self.vbox_history_chart = QtWidgets.QVBoxLayout(self.group_history_chart)
        self.vbox_history_chart.setObjectName("vbox_history_chart")
        self.chart_view_history = QtWidgets.QWidget(parent=self.group_history_chart)
        self.chart_view_history.setObjectName("chart_view_history")
        self.vbox_history_chart.addWidget(self.chart_view_history)
        self.vbox_history.addWidget(self.group_history_chart)
        self.group_history_details = QtWidgets.QGroupBox(parent=self.tab_history)
        self.group_history_details.setObjectName("group_history_details")
        self.vbox_history_details = QtWidgets.QVBoxLayout(self.group_history_details)
        self.vbox_history_details.setObjectName("vbox_history_details")
        self.table_history = QtWidgets.QTableWidget(parent=self.group_history_details)
        self.table_history.setObjectName("table_history")
        try:
            self.table_history.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))
        except Exception:
            pass
        hdr_hist = self.table_history.horizontalHeader()
        try:
            hdr_hist.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        except Exception:
            pass
        try:
            hdr_hist.setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        except Exception:
            pass
        try:
            self.table_history.verticalHeader().setVisible(False)
        except Exception:
            pass
        self.vbox_history_details.addWidget(self.table_history)
        self.vbox_history.addWidget(self.group_history_details)
        self.tabWidget.addTab(self.tab_history, "Prediction History")

        self.tab_map = QtWidgets.QWidget()
        self.tab_map.setObjectName("tab_map")
        self.vbox_map = QtWidgets.QVBoxLayout(self.tab_map)
        self.vbox_map.setObjectName("vbox_map")
        self.chart_view_city_map = QtWidgets.QWidget(parent=self.tab_map)
        self.chart_view_city_map.setObjectName("chart_view_city_map")
        self.vbox_map.addWidget(self.chart_view_city_map)
        self.tabWidget.addTab(self.tab_map, "Map")

        # Tab Recommendation (trước Chatbot)
        self.tab_recommend = QtWidgets.QWidget()
        self.tab_recommend.setObjectName("tab_recommend")
        self.vbox_recommend = QtWidgets.QVBoxLayout(self.tab_recommend)
        self.vbox_recommend.setObjectName("vbox_recommend")
        try:
            self.vbox_recommend.setSpacing(12)
        except Exception:
            pass
        # Form nhập yêu cầu người dùng
        self.lbl_recommend_input_title = QtWidgets.QLabel(parent=self.tab_recommend)
        self.lbl_recommend_input_title.setObjectName("lbl_recommend_input_title")
        self.lbl_recommend_input_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_recommend_input_title.setStyleSheet("color: #4c0c24; font-weight: 700; font-size: 18px; padding: 2px 6px;")
        self.vbox_recommend.addWidget(self.lbl_recommend_input_title)

        self.group_recommend_input = QtWidgets.QGroupBox(parent=self.tab_recommend)
        self.group_recommend_input.setObjectName("group_recommend_input")
        self.form_recommend = QtWidgets.QFormLayout(self.group_recommend_input)
        self.form_recommend.setObjectName("form_recommend")
        self.input_rec_budget = QtWidgets.QLineEdit(parent=self.group_recommend_input)
        self.input_rec_budget.setObjectName("input_rec_budget")
        self.input_rec_budget.setPlaceholderText("Example: 100,000 (USD)")
        self.form_recommend.addRow("Budget (USD)", self.input_rec_budget)
        self.input_rec_area = QtWidgets.QLineEdit(parent=self.group_recommend_input)
        self.input_rec_area.setObjectName("input_rec_area")
        self.input_rec_area.setPlaceholderText("Example: 80 (m²)")
        self.form_recommend.addRow("Floor area (m²)", self.input_rec_area)
        self.combo_rec_region = QtWidgets.QComboBox(parent=self.group_recommend_input)
        self.combo_rec_region.setObjectName("combo_rec_region")
        sp_combo = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.combo_rec_region.setSizePolicy(sp_combo)
        self.combo_rec_region.setMinimumWidth(360)
        self.combo_rec_region.setMinimumHeight(28)
        self.form_recommend.addRow("Region", self.combo_rec_region)
        self.combo_rec_type = QtWidgets.QComboBox(parent=self.group_recommend_input)
        self.combo_rec_type.setObjectName("combo_rec_type")
        self.combo_rec_type.addItems(["Optional", "Apartment", "Townhouse", "Villa"])  # thêm lựa chọn any
        self.form_recommend.addRow("Property type", self.combo_rec_type)
        self.btn_run_recommendation = QtWidgets.QPushButton(parent=self.group_recommend_input)
        self.btn_run_recommendation.setObjectName("btn_run_recommendation")
        self.btn_run_recommendation.setText("Run Recommendation")
        self.form_recommend.addRow(self.btn_run_recommendation)
        self.vbox_recommend.addWidget(self.group_recommend_input)
        # Bảng kết quả
        self.group_recommend_results = QtWidgets.QGroupBox(parent=self.tab_recommend)
        self.group_recommend_results.setObjectName("group_recommend_results")
        sizeExpand = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.group_recommend_results.setSizePolicy(sizeExpand)
        try:
            self.group_recommend_results.setFixedHeight(420)
        except Exception:
            pass
        self.vbox_recommend_results = QtWidgets.QVBoxLayout(self.group_recommend_results)
        self.vbox_recommend_results.setObjectName("vbox_recommend_results")
        self.table_recommendation = QtWidgets.QTableWidget(parent=self.group_recommend_results)
        self.table_recommendation.setObjectName("table_recommendation")
        self.table_recommendation.setColumnCount(7)
        self.table_recommendation.setHorizontalHeaderLabels(["Property Code", "Price", "Area", "Floor", "Match (%)", "Region", "Type"])
        self.table_recommendation.setAlternatingRowColors(True)
        self.table_recommendation.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_recommendation.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_recommendation.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))
        try:
            self.table_recommendation.setFixedHeight(360)
        except Exception:
            pass
        hdr = self.table_recommendation.horizontalHeader()
        try:
            hdr.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        except Exception:
            pass
        try:
            hdr.setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        except Exception:
            pass
        try:
            self.table_recommendation.verticalHeader().setVisible(False)
        except Exception:
            pass
        self.vbox_recommend_results.addWidget(self.table_recommendation)
        self.lbl_recommend_results_title = QtWidgets.QLabel(parent=self.tab_recommend)
        self.lbl_recommend_results_title.setObjectName("lbl_recommend_results_title")
        self.lbl_recommend_results_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_recommend_results_title.setStyleSheet("color: #4c0c24; font-weight: 700; font-size: 18px; padding: 2px 6px;")
        self.vbox_recommend.addWidget(self.lbl_recommend_results_title)
        self.vbox_recommend.addWidget(self.group_recommend_results, 1)
        try:
            self.vbox_recommend.addSpacing(12)
        except Exception:
            pass
        self.group_recommend_doc = QtWidgets.QGroupBox(parent=self.tab_recommend)
        self.group_recommend_doc.setObjectName("group_recommend_doc")
        self.vbox_recommend_doc = QtWidgets.QVBoxLayout(self.group_recommend_doc)
        self.vbox_recommend_doc.setObjectName("vbox_recommend_doc")
        self.group_recommend_doc.setContentsMargins(8, 0, 8, 8)
        self.vbox_recommend_doc.setContentsMargins(8, 0, 8, 8)
        self.txt_recommend_doc = QtWidgets.QLabel(parent=self.group_recommend_doc)
        self.txt_recommend_doc.setObjectName("txt_recommend_doc")
        self.txt_recommend_doc.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.txt_recommend_doc.setWordWrap(True)
        self.txt_recommend_doc.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.txt_recommend_doc.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))
        self.group_recommend_doc.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))
        self.group_recommend_doc.setStyleSheet("QLabel#txt_recommend_doc { background: #ffffff; color: #2b2342; padding: 12px; }")
        self.vbox_recommend_doc.addWidget(self.txt_recommend_doc)
        self.lbl_goal_title = QtWidgets.QLabel(parent=self.tab_recommend)
        self.lbl_goal_title.setObjectName("lbl_goal_title")
        self.lbl_goal_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        sp_caption = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.lbl_goal_title.setSizePolicy(sp_caption)
        self.lbl_goal_title.setMinimumHeight(40)
        self.lbl_goal_title.setStyleSheet(
            "QLabel#lbl_goal_title {"
            " background: #f8e1f4;"
            " color: #4c0c24;"
            " font-weight: 700;"
            " font-size: 18px;"
            " border: 1px solid #d6b6f5;"
            " border-radius: 8px;"
            " padding: 4px 8px;"
            "}"
        )
        self.vbox_recommend.addWidget(self.lbl_goal_title)
        self.vbox_recommend.addWidget(self.group_recommend_doc)
        try:
            self.vbox_recommend.setStretch(0, 0)
            self.vbox_recommend.setStretch(1, 0)
            self.vbox_recommend.setStretch(2, 0)
            self.vbox_recommend.setStretch(3, 1)
            self.vbox_recommend.setStretch(4, 0)
        except Exception:
            pass
        self.hbox_recommend_exports = QtWidgets.QHBoxLayout()
        self.hbox_recommend_exports.setObjectName("hbox_recommend_exports")
        self.btn_rec_export_csv = QtWidgets.QPushButton(parent=self.tab_recommend)
        self.btn_rec_export_csv.setObjectName("btn_rec_export_csv")
        self.btn_rec_export_pdf = QtWidgets.QPushButton(parent=self.tab_recommend)
        self.btn_rec_export_pdf.setObjectName("btn_rec_export_pdf")
        self.hbox_recommend_exports.addWidget(self.btn_rec_export_csv)
        self.hbox_recommend_exports.addWidget(self.btn_rec_export_pdf)
        self.vbox_recommend.addLayout(self.hbox_recommend_exports)
        self.tabWidget.addTab(self.tab_recommend, "Recommendation")

        # Tab Chatbot
        self.tab_chatbot = QtWidgets.QWidget()
        self.tab_chatbot.setObjectName("tab_chatbot")
        self.vbox_chatbot = QtWidgets.QVBoxLayout(self.tab_chatbot)
        self.vbox_chatbot.setObjectName("vbox_chatbot")
        self.group_chatbot = QtWidgets.QGroupBox(parent=self.tab_chatbot)
        self.group_chatbot.setObjectName("group_chatbot")
        self.vbox_group_chatbot = QtWidgets.QVBoxLayout(self.group_chatbot)
        self.vbox_group_chatbot.setObjectName("vbox_group_chatbot")
        self.btn_start_chatbot = QtWidgets.QPushButton(parent=self.group_chatbot)
        self.btn_start_chatbot.setObjectName("btn_start_chatbot")
        self.vbox_group_chatbot.addWidget(self.btn_start_chatbot)
        self.lbl_chatbot_url = QtWidgets.QLabel(parent=self.group_chatbot)
        self.lbl_chatbot_url.setObjectName("lbl_chatbot_url")
        self.lbl_chatbot_url.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.vbox_group_chatbot.addWidget(self.lbl_chatbot_url)
        self.widget_chatbot_web = QtWidgets.QWidget(parent=self.group_chatbot)
        self.widget_chatbot_web.setObjectName("widget_chatbot_web")
        self.vbox_group_chatbot.addWidget(self.widget_chatbot_web)
        self.vbox_chatbot.addWidget(self.group_chatbot)
        self.tabWidget.addTab(self.tab_chatbot, "Chatbot")

        CustomerHome.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=CustomerHome)
        self.menubar.setObjectName("menubar")
        CustomerHome.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=CustomerHome)
        self.statusbar.setObjectName("statusbar")
        CustomerHome.setStatusBar(self.statusbar)
        self.retranslateUi(CustomerHome)
        QtCore.QMetaObject.connectSlotsByName(CustomerHome)

    def retranslateUi(self, CustomerHome):
        _translate = QtCore.QCoreApplication.translate
        CustomerHome.setWindowTitle(_translate("CustomerHome", "Customer - ML Price Predictor"))
        self.lbl_header_title.setText(_translate("CustomerHome", "HOUSE PRICE PREDICTION SYSTEM"))
        self.btn_toggle_theme.setText(_translate("CustomerHome", "Toggle Theme"))
        self.btn_logout.setText(_translate("CustomerHome", "Logout"))
        # Đã bỏ khung Input Features và Results & Actions
        # Lịch sử
        self.group_history_actions = QtWidgets.QGroupBox(parent=self.tab_history)
        self.group_history_actions.setObjectName("group_history_actions")
        self.vbox_history_actions = QtWidgets.QVBoxLayout(self.group_history_actions)
        self.vbox_history_actions.setObjectName("vbox_history_actions")
        self.btn_delete_history = QtWidgets.QPushButton(parent=self.group_history_actions)
        self.btn_delete_history.setObjectName("btn_delete_history")
        self.vbox_history_actions.addWidget(self.btn_delete_history)
        self.btn_clear_history = QtWidgets.QPushButton(parent=self.group_history_actions)
        self.btn_clear_history.setObjectName("btn_clear_history")
        self.vbox_history_actions.addWidget(self.btn_clear_history)
        self.btn_export_history = QtWidgets.QPushButton(parent=self.group_history_actions)
        self.btn_export_history.setObjectName("btn_export_history")
        self.vbox_history_actions.addWidget(self.btn_export_history)
        self.vbox_history.addWidget(self.group_history_actions)
        self.group_history_chart.setTitle(_translate("CustomerHome", "Trend"))
        self.group_history_details.setTitle(_translate("CustomerHome", "Details"))
        self.group_history_actions.setTitle(_translate("CustomerHome", "Actions"))
        self.btn_delete_history.setText(_translate("CustomerHome", "Delete Selected"))
        self.btn_clear_history.setText(_translate("CustomerHome", "Clear All"))
        self.btn_export_history.setText(_translate("CustomerHome", "Export History (CSV)"))
        self.group_house_inline.setTitle(_translate("CustomerHome", "House Input Form"))
        self.group_price_chart.setTitle(_translate("CustomerHome", "Price Trend (2015–2035)"))
        self.group_chatbot.setTitle(_translate("CustomerHome", "House Price Advisory (Chatbot)"))
        self.btn_start_chatbot.setText(_translate("CustomerHome", "Start Chatbot"))
        self.lbl_chatbot_url.setText(_translate("CustomerHome", "URL: not started"))
        self.btn_export_csv.setText(_translate("CustomerHome", "Export CSV & XLSX"))
        self.btn_export_pdf.setText(_translate("CustomerHome", "Export PDF"))

        self.group_recommend_input.setTitle(_translate("CustomerHome", "User Input"))
        self.group_recommend_results.setTitle(_translate("CustomerHome", "Recommendations"))
        self.group_recommend_doc.setTitle("")
        self.lbl_goal_title.setText(_translate("CustomerHome", "Goal"))
        self.lbl_recommend_input_title.setText(_translate("CustomerHome", "User Input"))
        self.lbl_recommend_results_title.setText(_translate("CustomerHome", "Recommendations"))
        self.txt_recommend_doc.setText(_translate("CustomerHome", (
            "<div style=\"font-family: Segoe UI, sans-serif;\">"
            "<ul style=\"margin:0 0 6px 16px;\">"
            "<li>Suggest the Top 5 properties that best match the details you enter.</li>"
            "<li>Prioritize listings with strong fit across price, floor area, region, and property type.</li>"
            "<li>Help you quickly find options that align with your budget and preferences.</li>"
            "<li>Support decision‑making by comparing suitability scores across homes.</li>"
            "</ul>"
            "</div>"
        )))
        self.btn_rec_export_csv.setText(_translate("CustomerHome", "Export CSV & XLSX"))
        self.btn_rec_export_pdf.setText(_translate("CustomerHome", "Export PDF"))
        try:
            h = int(self.txt_recommend_doc.sizeHint().height()) + 12
            h = max(80, min(h, 200))
            self.txt_recommend_doc.setMinimumHeight(h)
            self.txt_recommend_doc.setMaximumHeight(h)
            self.group_recommend_doc.setMaximumHeight(h + 16)
        except Exception:
            pass