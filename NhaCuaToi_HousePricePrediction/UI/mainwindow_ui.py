# Form implementation generated from reading ui file 'MainWindow.ui'
# Created by: PyQt6 UI code generator
# WARNING: Any manual changes will be lost when pyuic6 is run again.

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 800)
        MainWindow.setWindowTitle("ML Price Predictor Studio")

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_central = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_central.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_central.setObjectName("verticalLayout_central")

        # THÊM: HBox ở trên cùng, chứa nút Toggle Theme
        self.hbox_theme_toggle = QtWidgets.QHBoxLayout()
        self.hbox_theme_toggle.setObjectName("hbox_theme_toggle")
        self.hbox_theme_toggle.addItem(
            QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        )
        self.btn_toggle_theme = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_toggle_theme.setObjectName("btn_toggle_theme")
        self.btn_toggle_theme.setText("Toggle Theme")
        self.hbox_theme_toggle.addWidget(self.btn_toggle_theme)
        self.verticalLayout_central.addLayout(self.hbox_theme_toggle)

        # QTabWidget như cũ
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)
        self.tabWidget.setDocumentMode(True)

        # --- Tab 1: Dataset ---
        self.tab_dataset = QtWidgets.QWidget()
        self.tab_dataset.setObjectName("tab_dataset")
        self.verticalLayout_tab1 = QtWidgets.QVBoxLayout(self.tab_dataset)
        self.verticalLayout_tab1.setSpacing(8)
        self.verticalLayout_tab1.setObjectName("verticalLayout_tab1")

        # Group 1: Config
        self.group_dataset_config = QtWidgets.QGroupBox(parent=self.tab_dataset)
        self.group_dataset_config.setObjectName("group_dataset_config")
        self.group_dataset_config.setTitle("1. Tải Dữ liệu & Cấu hình")
        self.gridLayout_dataset_config = QtWidgets.QGridLayout(self.group_dataset_config)
        self.gridLayout_dataset_config.setObjectName("gridLayout_dataset_config")

        self.label_choose_dataset = QtWidgets.QLabel(parent=self.group_dataset_config)
        self.label_choose_dataset.setObjectName("label_choose_dataset")
        self.label_choose_dataset.setText("Select Dataset:")
        self.gridLayout_dataset_config.addWidget(self.label_choose_dataset, 0, 0, 1, 1)

        self.combo_dataset = QtWidgets.QComboBox(parent=self.group_dataset_config)
        self.combo_dataset.setObjectName("combo_dataset")
        self.combo_dataset.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.gridLayout_dataset_config.addWidget(self.combo_dataset, 0, 1, 1, 1)

        sizeFixed = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.btn_pick_dataset = QtWidgets.QPushButton(parent=self.group_dataset_config)
        self.btn_pick_dataset.setObjectName("btn_pick_dataset")
        self.btn_pick_dataset.setText("Choose File...")
        self.btn_pick_dataset.setSizePolicy(sizeFixed)
        self.gridLayout_dataset_config.addWidget(self.btn_pick_dataset, 0, 2, 1, 1)

        self.label_train_rate = QtWidgets.QLabel(parent=self.group_dataset_config)
        self.label_train_rate.setObjectName("label_train_rate")
        self.label_train_rate.setText("Tỉ lệ Train (%):")
        self.gridLayout_dataset_config.addWidget(self.label_train_rate, 1, 0, 1, 1)

        self.spin_train_rate = QtWidgets.QSpinBox(parent=self.group_dataset_config)
        self.spin_train_rate.setObjectName("spin_train_rate")
        self.spin_train_rate.setMinimum(50)
        self.spin_train_rate.setMaximum(95)
        self.spin_train_rate.setValue(80)
        self.spin_train_rate.setSizePolicy(sizeFixed)
        self.gridLayout_dataset_config.addWidget(self.spin_train_rate, 1, 1, 1, 1)

        self.btn_load_and_train = QtWidgets.QPushButton(parent=self.group_dataset_config)
        self.btn_load_and_train.setObjectName("btn_load_and_train")
        self.btn_load_and_train.setText("Tải & Huấn luyện")
        self.btn_load_and_train.setSizePolicy(sizeFixed)
        self.gridLayout_dataset_config.addWidget(self.btn_load_and_train, 1, 2, 1, 1)

        self.gridLayout_dataset_config.setColumnStretch(0, 0)
        self.gridLayout_dataset_config.setColumnStretch(1, 1)
        self.gridLayout_dataset_config.setColumnStretch(2, 0)

        self.verticalLayout_tab1.addWidget(self.group_dataset_config)

        self.group_dataset_preview = QtWidgets.QGroupBox(parent=self.tab_dataset)
        self.group_dataset_preview.setTitle("2. Xem trước Dữ liệu")
        self.verticalLayout_preview = QtWidgets.QVBoxLayout(self.group_dataset_preview)
        self.verticalLayout_preview.setObjectName("verticalLayout_preview")

        sizeExpand = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.table_dataset_preview = QtWidgets.QTableWidget(parent=self.group_dataset_preview)
        self.table_dataset_preview.setObjectName("table_dataset_preview")
        self.table_dataset_preview.setSizePolicy(sizeExpand)
        self.table_dataset_preview.setColumnCount(0)
        self.table_dataset_preview.setRowCount(0)
        self.verticalLayout_preview.addWidget(self.table_dataset_preview)

        self.verticalLayout_tab1.addWidget(self.group_dataset_preview)

        self.lbl_status_tab1 = QtWidgets.QLabel(parent=self.tab_dataset)
        self.lbl_status_tab1.setObjectName("lbl_status_tab1")
        # ĐỔI TEXT: để trống
        self.lbl_status_tab1.setText("")
        self.verticalLayout_tab1.addWidget(self.lbl_status_tab1)

        self.verticalLayout_tab1.setStretch(0, 0)
        self.verticalLayout_tab1.setStretch(1, 1)
        self.verticalLayout_tab1.setStretch(2, 0)

        self.tabWidget.addTab(self.tab_dataset, "Dataset")

        # --- Tab 2: Kết quả Huấn luyện ---
        self.tab_train_results = QtWidgets.QWidget()
        self.tab_train_results.setObjectName("tab_train_results")
        self.hbox_train_results = QtWidgets.QHBoxLayout(self.tab_train_results)

        self.group_model_metrics = QtWidgets.QGroupBox(parent=self.tab_train_results)
        self.group_model_metrics.setTitle("Thông số Mô hình (Default: Linear Regression)")
        self.vbox_metrics = QtWidgets.QVBoxLayout(self.group_model_metrics)

        self.txt_model_metrics = QtWidgets.QTextEdit(parent=self.group_model_metrics)
        self.txt_model_metrics.setReadOnly(True)
        self.txt_model_metrics.setPlaceholderText("Coefficients, MAE, RMSE, R²...")
        self.txt_model_metrics.setSizePolicy(sizeExpand)
        self.vbox_metrics.addWidget(self.txt_model_metrics)

        self.btn_save_model = QtWidgets.QPushButton(parent=self.group_model_metrics)
        self.btn_save_model.setText("Lưu Model này")
        self.btn_save_model.setSizePolicy(sizeFixed)
        self.vbox_metrics.addWidget(self.btn_save_model)

        self.label_trained_models = QtWidgets.QLabel(parent=self.group_model_metrics)
        self.label_trained_models.setObjectName("label_trained_models")
        self.label_trained_models.setText("Chọn model đã huấn luyện:")
        self.vbox_metrics.addWidget(self.label_trained_models)

        self.combo_trained_models = QtWidgets.QComboBox(parent=self.group_model_metrics)
        self.combo_trained_models.setObjectName("combo_trained_models")
        self.combo_trained_models.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.vbox_metrics.addWidget(self.combo_trained_models)

        self.hbox_train_results.addWidget(self.group_model_metrics)

        self.group_train_results_table = QtWidgets.QGroupBox(parent=self.tab_train_results)
        self.group_train_results_table.setTitle("Test Set Results Table")
        self.vbox_train_table = QtWidgets.QVBoxLayout(self.group_train_results_table)

        self.table_train_results = QtWidgets.QTableWidget(parent=self.group_train_results_table)
        self.table_train_results.setObjectName("table_train_results")
        self.table_train_results.setSizePolicy(sizeExpand)
        self.table_train_results.setColumnCount(3)
        self.table_train_results.setRowCount(0)
        self.table_train_results.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem())
        self.table_train_results.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem())
        self.table_train_results.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem())
        self.vbox_train_table.addWidget(self.table_train_results)

        self.hbox_train_results.addWidget(self.group_train_results_table)

        self.hbox_train_results.setStretch(0, 1)
        self.hbox_train_results.setStretch(1, 2)

        self.tabWidget.addTab(self.tab_train_results, "Kết quả Huấn luyện")

        # --- Tab 3: So sánh Model ---
        self.tab_model_compare = QtWidgets.QWidget()
        self.tab_model_compare.setObjectName("tab_model_compare")
        self.hbox_compare = QtWidgets.QHBoxLayout(self.tab_model_compare)

        self.group_run_select_model = QtWidgets.QGroupBox(parent=self.tab_model_compare)
        self.group_run_select_model.setTitle("Run & Select Model")
        self.vbox_run_select = QtWidgets.QVBoxLayout(self.group_run_select_model)

        self.btn_evaluate_all_models = QtWidgets.QPushButton(parent=self.group_run_select_model)
        self.btn_evaluate_all_models.setText("Evaluate All Models")
        self.vbox_run_select.addWidget(self.btn_evaluate_all_models)

        self.table_model_comparison = QtWidgets.QTableWidget(parent=self.group_run_select_model)
        self.table_model_comparison.setObjectName("table_model_comparison")
        self.table_model_comparison.setSizePolicy(sizeExpand)
        self.table_model_comparison.setColumnCount(4)
        self.table_model_comparison.setRowCount(0)
        for i in range(4):
            self.table_model_comparison.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())
        self.vbox_run_select.addWidget(self.table_model_comparison)

        self.label_choose_best_model = QtWidgets.QLabel(parent=self.group_run_select_model)
        self.label_choose_best_model.setText("Choose Best Model (for Prediction):")
        self.vbox_run_select.addWidget(self.label_choose_best_model)

        self.combo_set_default_model = QtWidgets.QComboBox(parent=self.group_run_select_model)
        self.combo_set_default_model.setObjectName("combo_set_default_model")
        self.combo_set_default_model.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.vbox_run_select.addWidget(self.combo_set_default_model)

        self.hbox_compare.addWidget(self.group_run_select_model)

        self.group_analysis_charts = QtWidgets.QGroupBox(parent=self.tab_model_compare)
        self.group_analysis_charts.setTitle("Biểu đồ Phân tích")
        self.vbox_analysis_charts = QtWidgets.QVBoxLayout(self.group_analysis_charts)

        self.group_chart_compare = QtWidgets.QGroupBox(parent=self.group_analysis_charts)
        self.group_chart_compare.setTitle("Biểu đồ So sánh MAE/RMSE")
        self.vbox_chart_compare = QtWidgets.QVBoxLayout(self.group_chart_compare)

        self.chart_view_compare = QtWidgets.QWidget(parent=self.group_chart_compare)
        self.chart_view_compare.setObjectName("chart_view_compare")
        self.chart_view_compare.setSizePolicy(sizeExpand)
        self.vbox_chart_compare.addWidget(self.chart_view_compare)

        self.vbox_analysis_charts.addWidget(self.group_chart_compare)

        self.group_chart_residuals = QtWidgets.QGroupBox(parent=self.group_analysis_charts)
        self.group_chart_residuals.setTitle("Biểu đồ Phân phối Residuals (Model Mặc định)")
        self.vbox_chart_residuals = QtWidgets.QVBoxLayout(self.group_chart_residuals)

        self.chart_view_residuals_compare = QtWidgets.QWidget(parent=self.group_chart_residuals)
        self.chart_view_residuals_compare.setObjectName("chart_view_residuals_compare")
        self.chart_view_residuals_compare.setSizePolicy(sizeExpand)
        self.vbox_chart_residuals.addWidget(self.chart_view_residuals_compare)

        self.vbox_analysis_charts.addWidget(self.group_chart_residuals)

        self.btn_open_city_price_map = QtWidgets.QPushButton(parent=self.group_analysis_charts)
        self.btn_open_city_price_map.setText("Mở bản đồ giá theo tỉnh thành")
        self.vbox_analysis_charts.addWidget(self.btn_open_city_price_map)

        self.hbox_compare.addWidget(self.group_analysis_charts)
        self.hbox_compare.setStretch(0, 2)
        self.hbox_compare.setStretch(1, 1)

        self.tabWidget.addTab(self.tab_model_compare, "So sánh Model")

        # --- Tab 4: Dự đoán Giá ---
        self.tab_predict = QtWidgets.QWidget()
        self.tab_predict.setObjectName("tab_predict")
        self.hbox_predict = QtWidgets.QHBoxLayout(self.tab_predict)

        self.group_input_house = QtWidgets.QGroupBox(parent=self.tab_predict)
        self.group_input_house.setTitle("Nhập thông tin nhà")
        self.formLayout_inputs = QtWidgets.QFormLayout(self.group_input_house)

        self.label_income = QtWidgets.QLabel(parent=self.group_input_house)
        self.label_income.setText("Avg. Area Income:")
        self.input_area_income = QtWidgets.QLineEdit(parent=self.group_input_house)
        self.input_area_income.setObjectName("input_area_income")
        self.input_area_income.setPlaceholderText("e.g., 65000")
        self.input_area_income.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.formLayout_inputs.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_income)
        self.formLayout_inputs.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.input_area_income)

        self.label_house_age = QtWidgets.QLabel(parent=self.group_input_house)
        self.label_house_age.setText("Avg. Area House Age:")
        self.input_house_age = QtWidgets.QLineEdit(parent=self.group_input_house)
        self.input_house_age.setObjectName("input_house_age")
        self.input_house_age.setPlaceholderText("e.g., 5.2")
        self.input_house_age.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.formLayout_inputs.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_house_age)
        self.formLayout_inputs.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.input_house_age)

        self.label_num_rooms = QtWidgets.QLabel(parent=self.group_input_house)
        self.label_num_rooms.setText("Avg. Area Number of Rooms:")
        self.input_num_rooms = QtWidgets.QLineEdit(parent=self.group_input_house)
        self.input_num_rooms.setObjectName("input_num_rooms")
        self.input_num_rooms.setPlaceholderText("e.g., 6.0")
        self.input_num_rooms.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.formLayout_inputs.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_num_rooms)
        self.formLayout_inputs.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.input_num_rooms)

        self.label_num_bedrooms = QtWidgets.QLabel(parent=self.group_input_house)
        self.label_num_bedrooms.setText("Avg. Area Number of Bedrooms:")
        self.input_num_bedrooms = QtWidgets.QLineEdit(parent=self.group_input_house)
        self.input_num_bedrooms.setObjectName("input_num_bedrooms")
        self.input_num_bedrooms.setPlaceholderText("e.g., 3.0")
        self.input_num_bedrooms.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.formLayout_inputs.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_num_bedrooms)
        self.formLayout_inputs.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.input_num_bedrooms)

        self.label_population = QtWidgets.QLabel(parent=self.group_input_house)
        self.label_population.setText("Area Population:")
        self.input_population = QtWidgets.QLineEdit(parent=self.group_input_house)
        self.input_population.setObjectName("input_population")
        self.input_population.setPlaceholderText("e.g., 300000")
        self.input_population.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.formLayout_inputs.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_population)
        self.formLayout_inputs.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.input_population)

        self.hbox_predict.addWidget(self.group_input_house)

        self.group_predict_actions = QtWidgets.QGroupBox(parent=self.tab_predict)
        self.group_predict_actions.setTitle("Kết quả & Tác vụ")
        self.vbox_predict_actions = QtWidgets.QVBoxLayout(self.group_predict_actions)

        self.group_current_model = QtWidgets.QGroupBox(parent=self.group_predict_actions)
        self.group_current_model.setTitle("Thông tin Model Đang Dùng")
        self.vbox_current_model = QtWidgets.QVBoxLayout(self.group_current_model)
        self.lbl_current_model = QtWidgets.QLabel(parent=self.group_current_model)
        self.lbl_current_model.setText("Model:")
        self.vbox_current_model.addWidget(self.lbl_current_model)
        self.lbl_current_model_mae = QtWidgets.QLabel(parent=self.group_current_model)
        self.lbl_current_model_mae.setText("MAE:")
        self.vbox_current_model.addWidget(self.lbl_current_model_mae)
        self.lbl_current_model_rmse = QtWidgets.QLabel(parent=self.group_current_model)
        self.lbl_current_model_rmse.setText("RMSE:")
        self.vbox_current_model.addWidget(self.lbl_current_model_rmse)
        self.vbox_predict_actions.addWidget(self.group_current_model)

        self.btn_quick_evaluate = QtWidgets.QPushButton(parent=self.group_predict_actions)
        self.btn_quick_evaluate.setText("Đánh giá nhanh")
        self.btn_quick_evaluate.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.vbox_predict_actions.addWidget(self.btn_quick_evaluate)

        self.btn_predict = QtWidgets.QPushButton(parent=self.group_predict_actions)
        self.btn_predict.setText("Predict Price")
        self.btn_predict.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.vbox_predict_actions.addWidget(self.btn_predict)

        self.label_pred_price = QtWidgets.QLabel(parent=self.group_predict_actions)
        self.label_pred_price.setText("Predicted Price:")
        self.vbox_predict_actions.addWidget(self.label_pred_price)

        self.lbl_prediction_result = QtWidgets.QLabel(parent=self.group_predict_actions)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.lbl_prediction_result.setFont(font)
        self.lbl_prediction_result.setText("...")
        self.lbl_prediction_result.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.vbox_predict_actions.addWidget(self.lbl_prediction_result)

        self.btn_export_report = QtWidgets.QPushButton(parent=self.group_predict_actions)
        self.btn_export_report.setText("Export Report (CSV)")
        self.btn_export_report.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.vbox_predict_actions.addWidget(self.btn_export_report)

        self.btn_open_house_input_form = QtWidgets.QPushButton(parent=self.group_predict_actions)
        self.btn_open_house_input_form.setText("Open House Input Form")
        self.btn_open_house_input_form.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.vbox_predict_actions.addWidget(self.btn_open_house_input_form)

        self.vbox_predict_actions.setStretch(0, 0)
        self.vbox_predict_actions.setStretch(1, 0)
        self.vbox_predict_actions.setStretch(2, 0)
        self.vbox_predict_actions.setStretch(3, 0)
        self.vbox_predict_actions.setStretch(4, 1)
        self.vbox_predict_actions.setStretch(5, 0)
        self.vbox_predict_actions.setStretch(5, 0)

        self.hbox_predict.addWidget(self.group_predict_actions)
        self.hbox_predict.setStretch(0, 1)
        self.hbox_predict.setStretch(1, 2)

        self.tabWidget.addTab(self.tab_predict, "Dự đoán Giá")

        # --- Tab 5: Lịch sử Dự đoán ---
        self.tab_history = QtWidgets.QWidget()
        self.vbox_history = QtWidgets.QVBoxLayout(self.tab_history)

        self.group_history_chart = QtWidgets.QGroupBox(parent=self.tab_history)
        self.group_history_chart.setTitle("History Trend Chart")
        self.vbox_history_chart = QtWidgets.QVBoxLayout(self.group_history_chart)
        self.chart_view_history = QtWidgets.QWidget(parent=self.group_history_chart)
        self.chart_view_history.setObjectName("chart_view_history")
        self.chart_view_history.setSizePolicy(sizeExpand)
        self.vbox_history_chart.addWidget(self.chart_view_history)
        self.vbox_history.addWidget(self.group_history_chart)

        self.group_history_details = QtWidgets.QGroupBox(parent=self.tab_history)
        self.group_history_details.setTitle("History Details")
        self.vbox_history_details = QtWidgets.QVBoxLayout(self.group_history_details)

        self.table_history = QtWidgets.QTableWidget(parent=self.group_history_details)
        self.table_history.setObjectName("table_history")
        self.table_history.setSizePolicy(sizeExpand)
        self.table_history.setColumnCount(4)
        self.table_history.setRowCount(0)
        for i in range(4):
            self.table_history.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())
        self.vbox_history_details.addWidget(self.table_history)

        self.group_history_actions = QtWidgets.QGroupBox(parent=self.group_history_details)
        self.group_history_actions.setTitle("Actions")
        self.hbox_history_actions = QtWidgets.QHBoxLayout(self.group_history_actions)

        self.btn_delete_history = QtWidgets.QPushButton(parent=self.group_history_actions)
        self.btn_delete_history.setText("Delete Selected")
        self.btn_delete_history.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.hbox_history_actions.addWidget(self.btn_delete_history)

        self.btn_clear_history = QtWidgets.QPushButton(parent=self.group_history_actions)
        self.btn_clear_history.setText("Clear All")
        self.btn_clear_history.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.hbox_history_actions.addWidget(self.btn_clear_history)

        self.btn_export_history = QtWidgets.QPushButton(parent=self.group_history_actions)
        self.btn_export_history.setText("Export History (CSV)")
        self.btn_export_history.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.hbox_history_actions.addWidget(self.btn_export_history)

        self.hbox_history_actions.setStretch(0, 1)
        self.hbox_history_actions.setStretch(1, 1)
        self.hbox_history_actions.setStretch(2, 1)

        self.vbox_history_details.addWidget(self.group_history_actions)
        self.vbox_history.addWidget(self.group_history_details)
        self.vbox_history.setStretch(0, 2)
        self.vbox_history.setStretch(1, 1)

        self.tabWidget.addTab(self.tab_history, "Prediction History")

        self.verticalLayout_central.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        # Menubar (hidden)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.setVisible(False)

        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Header texts for tables
        # Tab 2 table headers
        item = self.table_train_results.horizontalHeaderItem(0)
        item.setText(QtCore.QCoreApplication.translate("MainWindow", "Actual Value"))
        item = self.table_train_results.horizontalHeaderItem(1)
        item.setText(QtCore.QCoreApplication.translate("MainWindow", "Predicted Value"))

        # Tab 3 table headers
        item = self.table_model_comparison.horizontalHeaderItem(0)
        item.setText(QtCore.QCoreApplication.translate("MainWindow", "Model"))
        item = self.table_model_comparison.horizontalHeaderItem(1)
        item.setText(QtCore.QCoreApplication.translate("MainWindow", "MAE"))
        item = self.table_model_comparison.horizontalHeaderItem(2)
        item.setText(QtCore.QCoreApplication.translate("MainWindow", "RMSE"))
        item = self.table_model_comparison.horizontalHeaderItem(3)
        item.setText(QtCore.QCoreApplication.translate("MainWindow", "R²"))

        # Tab 5 table headers
        item = self.table_history.horizontalHeaderItem(0)
        item.setText(QtCore.QCoreApplication.translate("MainWindow", "Time"))
        item = self.table_history.horizontalHeaderItem(1)
        item.setText(QtCore.QCoreApplication.translate("MainWindow", "Input Summary"))
        item = self.table_history.horizontalHeaderItem(2)
        item.setText(QtCore.QCoreApplication.translate("MainWindow", "Predicted Price"))
        item = self.table_history.horizontalHeaderItem(3)
        item.setText(QtCore.QCoreApplication.translate("MainWindow", "Model"))

        # Layout stretches ensuring space fill
        self.vbox_metrics.setStretch(0, 1)
        self.vbox_metrics.setStretch(1, 0)

    def retranslateUi(self, MainWindow):
        # Provided above; kept minimal since texts are already set
        pass