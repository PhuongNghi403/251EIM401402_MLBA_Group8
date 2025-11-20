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

        # Topbar widget với tiêu đề giữa và nút Toggle Theme
        self.widget_topbar = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget_topbar.setObjectName("widget_topbar")
        self.hbox_theme_toggle = QtWidgets.QHBoxLayout(self.widget_topbar)
        self.hbox_theme_toggle.setObjectName("hbox_theme_toggle")
        self.hbox_theme_toggle.setContentsMargins(12, 8, 12, 8)
        left_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hbox_theme_toggle.addItem(left_spacer)
        self.lbl_header_title = QtWidgets.QLabel(parent=self.widget_topbar)
        self.lbl_header_title.setObjectName("lbl_header_title")
        self.lbl_header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_header_title.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred))
        _hdr_font = QtGui.QFont()
        _hdr_font.setPointSize(20)
        self.lbl_header_title.setFont(_hdr_font)
        self.hbox_theme_toggle.addWidget(self.lbl_header_title)
        right_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hbox_theme_toggle.addItem(right_spacer)
        self.btn_toggle_theme = QtWidgets.QPushButton(parent=self.widget_topbar)
        self.btn_toggle_theme.setObjectName("btn_toggle_theme")
        self.btn_toggle_theme.setText("Toggle Theme")
        self.hbox_theme_toggle.addWidget(self.btn_toggle_theme)

        self.btn_logout = QtWidgets.QPushButton(parent=self.widget_topbar)
        self.btn_logout.setObjectName("btn_logout")
        self.btn_logout.setText("Log Out")
        self.hbox_theme_toggle.addWidget(self.btn_logout)
        self.verticalLayout_central.addWidget(self.widget_topbar)

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
        self.group_dataset_config.setTitle("Load Dataset & Config")
        self.group_dataset_config.setStyleSheet("QGroupBox { margin-top: 24px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; font-weight: 900; font-size: 12px; color: #4c0c24; padding: 2px 10px; }")
        font_ds_title = QtGui.QFont()
        font_ds_title.setPointSize(12)
        font_ds_title.setBold(True)
        self.group_dataset_config.setFont(font_ds_title)
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
        self.label_train_rate.setText("Train Rate (%):")
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
        self.btn_load_and_train.setText("Load and Train")
        self.btn_load_and_train.setSizePolicy(sizeFixed)
        self.gridLayout_dataset_config.addWidget(self.btn_load_and_train, 1, 2, 1, 1)

        self.gridLayout_dataset_config.setColumnStretch(0, 0)
        self.gridLayout_dataset_config.setColumnStretch(1, 1)
        self.gridLayout_dataset_config.setColumnStretch(2, 0)

        self.verticalLayout_tab1.addWidget(self.group_dataset_config)

        self.group_dataset_preview = QtWidgets.QGroupBox(parent=self.tab_dataset)
        self.group_dataset_preview.setTitle("Preview Dataset")
        self.group_dataset_preview.setStyleSheet("QGroupBox { margin-top: 24px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; font-weight: 900; font-size: 12px; color: #4c0c24; padding: 2px 10px; }")
        self.group_dataset_preview.setFont(font_ds_title)
        self.verticalLayout_preview = QtWidgets.QVBoxLayout(self.group_dataset_preview)
        self.verticalLayout_preview.setObjectName("verticalLayout_preview")

        sizeExpand = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.table_dataset_preview = QtWidgets.QTableWidget(parent=self.group_dataset_preview)
        self.table_dataset_preview.setObjectName("table_dataset_preview")
        self.table_dataset_preview.setSizePolicy(sizeExpand)
        self.table_dataset_preview.setColumnCount(0)
        self.table_dataset_preview.setRowCount(0)
        try:
            hdr_ds = self.table_dataset_preview.horizontalHeader()
            hdr_ds.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        except Exception:
            pass
        try:
            self.table_dataset_preview.verticalHeader().setVisible(False)
        except Exception:
            pass
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
        self.group_model_metrics.setTitle("Model Metrics (Default: Linear Regression)")
        self.group_model_metrics.setStyleSheet("QGroupBox { margin-top: 24px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; font-weight: 900; font-size: 12px; color: #4c0c24; padding: 2px 10px; }")
        font_group12 = QtGui.QFont()
        font_group12.setPointSize(12)
        font_group12.setBold(True)
        self.group_model_metrics.setFont(font_group12)
        self.vbox_metrics = QtWidgets.QVBoxLayout(self.group_model_metrics)

        self.txt_model_metrics = QtWidgets.QTextEdit(parent=self.group_model_metrics)
        self.txt_model_metrics.setReadOnly(True)
        self.txt_model_metrics.setPlaceholderText("Coefficients, MAE, RMSE, R²...")
        self.txt_model_metrics.setSizePolicy(sizeExpand)
        self.vbox_metrics.addWidget(self.txt_model_metrics)

        self.btn_save_model = QtWidgets.QPushButton(parent=self.group_model_metrics)
        self.btn_save_model.setText("Save Model")
        self.btn_save_model.setSizePolicy(sizeFixed)
        self.vbox_metrics.addWidget(self.btn_save_model)

        self.group_select_trained = QtWidgets.QGroupBox(parent=self.group_model_metrics)
        self.group_select_trained.setTitle("Select Trained Model")
        self.group_select_trained.setStyleSheet("QGroupBox { margin-top: 24px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; font-weight: 900; font-size: 12px; color: #4c0c24; padding: 2px 10px; }")
        self.vbox_select_trained = QtWidgets.QVBoxLayout(self.group_select_trained)
        
        self.combo_trained_models = QtWidgets.QComboBox(parent=self.group_select_trained)
        self.combo_trained_models.setObjectName("combo_trained_models")
        self.combo_trained_models.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.vbox_select_trained.addWidget(self.combo_trained_models)
        self.vbox_metrics.addWidget(self.group_select_trained)

        self.hbox_train_results.addWidget(self.group_model_metrics)

        self.group_train_results_table = QtWidgets.QGroupBox(parent=self.tab_train_results)
        self.group_train_results_table.setTitle("Test Set Results Table")
        self.group_train_results_table.setStyleSheet("QGroupBox { margin-top: 24px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; font-weight: 900; font-size: 12px; color: #4c0c24; padding: 2px 10px; }")
        self.group_train_results_table.setFont(font_group12)
        self.vbox_train_table = QtWidgets.QVBoxLayout(self.group_train_results_table)

        self.table_train_results = QtWidgets.QTableWidget(parent=self.group_train_results_table)
        self.table_train_results.setObjectName("table_train_results")
        self.table_train_results.setSizePolicy(sizeExpand)
        self.table_train_results.setColumnCount(3)
        self.table_train_results.setRowCount(0)
        self.table_train_results.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem())
        self.table_train_results.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem())
        self.table_train_results.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem())
        try:
            hdr_tr = self.table_train_results.horizontalHeader()
            hdr_tr.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        except Exception:
            pass
        try:
            self.table_train_results.verticalHeader().setVisible(False)
        except Exception:
            pass
        self.vbox_train_table.addWidget(self.table_train_results)

        self.hbox_train_results.addWidget(self.group_train_results_table)

        self.hbox_train_results.setStretch(0, 1)
        self.hbox_train_results.setStretch(1, 2)

        self.tabWidget.addTab(self.tab_train_results, "Train Results")

        # --- Tab 3: So sánh Model ---
        self.tab_model_compare = QtWidgets.QWidget()
        self.tab_model_compare.setObjectName("tab_model_compare")
        self.hbox_compare = QtWidgets.QHBoxLayout(self.tab_model_compare)

        self.group_run_select_model = QtWidgets.QGroupBox(parent=self.tab_model_compare)
        self.group_run_select_model.setTitle("Run & Select Model")
        self.group_run_select_model.setStyleSheet("QGroupBox { margin-top: 24px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; font-weight: 900; font-size: 12px; color: #4c0c24; padding: 2px 10px; }")
        font_mc_title = QtGui.QFont()
        font_mc_title.setPointSize(12)
        font_mc_title.setBold(True)
        self.group_run_select_model.setFont(font_mc_title)
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
        try:
            hdr_mc = self.table_model_comparison.horizontalHeader()
            hdr_mc.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        except Exception:
            pass
        try:
            self.table_model_comparison.verticalHeader().setVisible(False)
        except Exception:
            pass
        self.vbox_run_select.addWidget(self.table_model_comparison)

        

        self.hbox_compare.addWidget(self.group_run_select_model)

        self.group_analysis_charts = QtWidgets.QGroupBox(parent=self.tab_model_compare)
        self.group_analysis_charts.setTitle("Analysis Charts")
        self.group_analysis_charts.setStyleSheet("QGroupBox { margin-top: 24px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; font-weight: 900; font-size: 12px; color: #4c0c24; padding: 2px 10px; }")
        self.group_analysis_charts.setFont(font_mc_title)
        self.vbox_analysis_charts = QtWidgets.QVBoxLayout(self.group_analysis_charts)
        self.analysis_scroll_area = QtWidgets.QScrollArea(parent=self.group_analysis_charts)
        self.analysis_scroll_area.setObjectName("analysis_scroll_area")
        self.analysis_scroll_area.setWidgetResizable(True)
        self.analysis_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.analysis_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.analysis_scroll_area.setMinimumHeight(520)
        self.analysis_scroll_area.setMaximumHeight(520)
        self.analysis_scroll_contents = QtWidgets.QWidget()
        self.analysis_scroll_contents.setObjectName("analysis_scroll_contents")
        self.vbox_analysis_scroll = QtWidgets.QVBoxLayout(self.analysis_scroll_contents)

        self.group_chart_compare = QtWidgets.QGroupBox(parent=self.analysis_scroll_contents)
        self.group_chart_compare.setTitle("Model Comparison Charts")
        self.vbox_chart_compare = QtWidgets.QVBoxLayout(self.group_chart_compare)
        self.group_chart_compare.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))
        self.group_chart_compare.setMinimumHeight(280)

        self.chart_view_compare = QtWidgets.QWidget(parent=self.group_chart_compare)
        self.chart_view_compare.setObjectName("chart_view_compare")
        self.chart_view_compare.setSizePolicy(sizeExpand)
        self.chart_view_compare.setMinimumHeight(240)
        self.vbox_chart_compare.addWidget(self.chart_view_compare)

        self.vbox_analysis_scroll.addWidget(self.group_chart_compare)

        self.group_chart_residuals = QtWidgets.QGroupBox(parent=self.analysis_scroll_contents)
        self.group_chart_residuals.setTitle("Detailed Analysis Charts (Selected Model)")
        self.vbox_chart_residuals = QtWidgets.QVBoxLayout(self.group_chart_residuals)
        self.group_chart_residuals.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))
        self.group_chart_residuals.setMinimumHeight(800)

        self.chart_view_actual_pred = QtWidgets.QWidget(parent=self.group_chart_residuals)
        self.chart_view_actual_pred.setObjectName("chart_view_actual_pred")
        self.chart_view_actual_pred.setSizePolicy(sizeExpand)
        self.chart_view_actual_pred.setMinimumHeight(240)
        self.vbox_chart_residuals.addWidget(self.chart_view_actual_pred)

        self.chart_view_residuals_compare = QtWidgets.QWidget(parent=self.group_chart_residuals)
        self.chart_view_residuals_compare.setObjectName("chart_view_residuals_compare")
        self.chart_view_residuals_compare.setSizePolicy(sizeExpand)
        self.chart_view_residuals_compare.setMinimumHeight(240)
        self.vbox_chart_residuals.addWidget(self.chart_view_residuals_compare)

        self.chart_view_feature_importance = QtWidgets.QWidget(parent=self.group_chart_residuals)
        self.chart_view_feature_importance.setObjectName("chart_view_feature_importance")
        self.chart_view_feature_importance.setSizePolicy(sizeExpand)
        self.chart_view_feature_importance.setMinimumHeight(240)
        self.vbox_chart_residuals.addWidget(self.chart_view_feature_importance)

        self.vbox_analysis_scroll.addWidget(self.group_chart_residuals)
        self.analysis_scroll_area.setWidget(self.analysis_scroll_contents)
        self.vbox_analysis_charts.addWidget(self.analysis_scroll_area)

        self.btn_open_city_price_map = QtWidgets.QPushButton(parent=self.group_analysis_charts)
        self.btn_open_city_price_map.setText("Open City Price Map")
        self.vbox_analysis_charts.addWidget(self.btn_open_city_price_map)

        self.hbox_compare.addWidget(self.group_analysis_charts)
        self.hbox_compare.setStretch(0, 1)
        self.hbox_compare.setStretch(1, 3)

        self.tabWidget.addTab(self.tab_model_compare, "Model Comparison")

        # --- Tab 4: Dự đoán Giá ---
        self.tab_predict = QtWidgets.QWidget()
        self.tab_predict.setObjectName("tab_predict")
        self.hbox_predict = QtWidgets.QHBoxLayout(self.tab_predict)

        self.group_input_house = QtWidgets.QGroupBox(parent=self.tab_predict)
        self.group_input_house.setTitle("Input House Information")
        self.group_input_house.setStyleSheet("QGroupBox { margin-top: 24px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; font-weight: 900; font-size: 12px; color: #4c0c24; padding: 2px 10px; }")
        font_group_title = QtGui.QFont()
        font_group_title.setPointSize(12)
        font_group_title.setBold(True)
        self.group_input_house.setFont(font_group_title)
        self.formLayout_inputs = QtWidgets.QFormLayout(self.group_input_house)

        self.label_area = QtWidgets.QLabel(parent=self.group_input_house)
        self.label_area.setText("Area:")
        self.input_area = QtWidgets.QLineEdit(parent=self.group_input_house)
        self.input_area.setObjectName("input_area")
        self.input_area.setPlaceholderText("e.g., 80.0")
        self.input_area.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.formLayout_inputs.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_area)
        self.formLayout_inputs.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.input_area)

        self.label_frontage = QtWidgets.QLabel(parent=self.group_input_house)
        self.label_frontage.setText("Frontage:")
        self.input_frontage = QtWidgets.QLineEdit(parent=self.group_input_house)
        self.input_frontage.setObjectName("input_frontage")
        self.input_frontage.setPlaceholderText("e.g., 5.0")
        self.input_frontage.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.formLayout_inputs.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_frontage)
        self.formLayout_inputs.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.input_frontage)

        self.label_floors = QtWidgets.QLabel(parent=self.group_input_house)
        self.label_floors.setText("Floors:")
        self.input_floors = QtWidgets.QLineEdit(parent=self.group_input_house)
        self.input_floors.setObjectName("input_floors")
        self.input_floors.setPlaceholderText("e.g., 3")
        self.input_floors.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.formLayout_inputs.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_floors)
        self.formLayout_inputs.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.input_floors)

        self.label_bedrooms = QtWidgets.QLabel(parent=self.group_input_house)
        self.label_bedrooms.setText("Bedrooms:")
        self.input_bedrooms = QtWidgets.QLineEdit(parent=self.group_input_house)
        self.input_bedrooms.setObjectName("input_bedrooms")
        self.input_bedrooms.setPlaceholderText("e.g., 3")
        self.input_bedrooms.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.formLayout_inputs.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_bedrooms)
        self.formLayout_inputs.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.input_bedrooms)

        self.label_bathrooms = QtWidgets.QLabel(parent=self.group_input_house)
        self.label_bathrooms.setText("Bathrooms:")
        self.input_bathrooms = QtWidgets.QLineEdit(parent=self.group_input_house)
        self.input_bathrooms.setObjectName("input_bathrooms")
        self.input_bathrooms.setPlaceholderText("e.g., 2")
        self.input_bathrooms.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.formLayout_inputs.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_bathrooms)
        self.formLayout_inputs.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.input_bathrooms)

        self.lbl_house_image = QtWidgets.QLabel(parent=self.group_input_house)
        self.lbl_house_image.setObjectName("lbl_house_image")
        self.lbl_house_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_house_image.setMinimumHeight(240)
        self.lbl_house_image.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding))
        try:
            import os
            img_base = os.path.dirname(os.path.dirname(__file__))
            img_path = os.path.join(img_base, "ttad.png")
            pix = QtGui.QPixmap(img_path)
            if pix and not pix.isNull():
                self.lbl_house_image.setPixmap(pix.scaled(480, 320, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
        except Exception:
            pass
        self.formLayout_inputs.addRow(self.lbl_house_image)

        self.hbox_predict.addWidget(self.group_input_house)

        self.group_predict_actions = QtWidgets.QGroupBox(parent=self.tab_predict)
        self.group_predict_actions.setTitle("Prediction Results: Actions")
        self.group_predict_actions.setStyleSheet("QGroupBox { margin-top: 24px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; font-weight: 900; font-size: 12px; color: #4c0c24; padding: 2px 10px; }")
        self.group_predict_actions.setFont(font_group_title)
        self.vbox_predict_actions = QtWidgets.QVBoxLayout(self.group_predict_actions)
        # Hàng chọn model mặc định đặt lên đầu và thu gọn khoảng cách
        self.hbox_default_model = QtWidgets.QHBoxLayout()
        self.hbox_default_model.setContentsMargins(6, 4, 6, 4)
        self.hbox_default_model.setSpacing(6)
        self.label_choose_best_model = QtWidgets.QLabel(parent=self.group_predict_actions)
        self.label_choose_best_model.setText("Choose Best Model (for Prediction):")
        self.hbox_default_model.addWidget(self.label_choose_best_model)
        self.combo_set_default_model = QtWidgets.QComboBox(parent=self.group_predict_actions)
        self.combo_set_default_model.setObjectName("combo_set_default_model")
        self.combo_set_default_model.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.hbox_default_model.addWidget(self.combo_set_default_model)
        self.vbox_predict_actions.addLayout(self.hbox_default_model)

        self.group_current_model = QtWidgets.QGroupBox(parent=self.group_predict_actions)
        self.group_current_model.setTitle("Current Model Information")
        self.group_current_model.setStyleSheet("QGroupBox { margin-top: 24px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; font-size: 12px; color: #4c0c24; padding: 2px 10px; }")
        font_title12 = QtGui.QFont()
        font_title12.setPointSize(12)
        font_title12.setBold(False)
        self.group_current_model.setFont(font_title12)
        self.group_current_model.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.group_current_model.setMaximumHeight(220)
        self.vbox_current_model = QtWidgets.QVBoxLayout(self.group_current_model)
        self.vbox_current_model.setContentsMargins(12, 10, 12, 10)
        self.vbox_current_model.setSpacing(8)
        # Tăng cỡ chữ và làm đậm cho các label thông tin
        font_info = QtGui.QFont()
        font_info.setPointSize(12)
        font_info.setBold(True)
        self.lbl_current_model = QtWidgets.QLabel(parent=self.group_current_model)
        self.lbl_current_model.setText("Model:")
        self.lbl_current_model.setFont(font_info)
        self.lbl_current_model.setStyleSheet("color: #000000;")
        self.vbox_current_model.addWidget(self.lbl_current_model)
        self.lbl_current_model_mae = QtWidgets.QLabel(parent=self.group_current_model)
        self.lbl_current_model_mae.setText("MAE:")
        self.lbl_current_model_mae.setFont(font_info)
        self.lbl_current_model_mae.setStyleSheet("color: #000000;")
        self.vbox_current_model.addWidget(self.lbl_current_model_mae)
        self.lbl_current_model_rmse = QtWidgets.QLabel(parent=self.group_current_model)
        self.lbl_current_model_rmse.setText("RMSE:")
        self.lbl_current_model_rmse.setFont(font_info)
        self.lbl_current_model_rmse.setStyleSheet("color: #000000;")
        self.vbox_current_model.addWidget(self.lbl_current_model_rmse)
        self.vbox_predict_actions.addWidget(self.group_current_model)


        # Group: Quick Prediction (contains Predict button and caption label)
        self.group_quick_predict = QtWidgets.QGroupBox(parent=self.group_predict_actions)
        self.group_quick_predict.setTitle("Quick Prediction")
        self.group_quick_predict.setStyleSheet("QGroupBox { margin-top: 24px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; font-size: 12px; color: #4c0c24; padding: 2px 10px; }")
        self.group_quick_predict.setFont(font_title12)
        # Giới hạn chiều cao để group box gọn gàng và không nở quá lớn
        self.group_quick_predict.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.group_quick_predict.setMaximumHeight(200)
        self.vbox_quick_predict = QtWidgets.QVBoxLayout(self.group_quick_predict)
        self.vbox_quick_predict.setContentsMargins(8, 6, 8, 6)
        self.vbox_quick_predict.setSpacing(8)

        self.btn_predict = QtWidgets.QPushButton(parent=self.group_quick_predict)
        self.btn_predict.setText("Predict Price")
        self.btn_predict.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.vbox_quick_predict.addWidget(self.btn_predict)

        self.label_pred_price = QtWidgets.QLabel(parent=self.group_quick_predict)
        font_caption = QtGui.QFont()
        font_caption.setPointSize(11)
        font_caption.setBold(True)
        self.label_pred_price.setFont(font_caption)
        self.label_pred_price.setText("Predicted Price:")
        self.label_pred_price.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.vbox_quick_predict.addWidget(self.label_pred_price)

        self.vbox_predict_actions.addWidget(self.group_quick_predict)

        self.lbl_prediction_result = QtWidgets.QLabel(parent=self.group_quick_predict)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.lbl_prediction_result.setFont(font)
        self.lbl_prediction_result.setText("...")
        self.lbl_prediction_result.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed))
        self.lbl_prediction_result.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.vbox_quick_predict.addWidget(self.lbl_prediction_result)

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
        self.vbox_predict_actions.setStretch(4, 0)
        self.vbox_predict_actions.setStretch(5, 1)
        self.vbox_predict_actions.setStretch(6, 0)
        self.vbox_predict_actions.setStretch(7, 0)

        self.hbox_predict.addWidget(self.group_predict_actions)
        self.hbox_predict.setStretch(0, 1)
        self.hbox_predict.setStretch(1, 2)

        self.tabWidget.addTab(self.tab_predict, "Price Prediction")

        # --- Tab 5: Lịch sử Dự đoán ---
        self.tab_history = QtWidgets.QWidget()
        self.vbox_history = QtWidgets.QVBoxLayout(self.tab_history)

        # History Trend Chart removed per request

        self.group_history_chart = QtWidgets.QGroupBox(parent=self.tab_history)
        self.group_history_chart.setTitle("History Trend Chart")
        self.group_history_chart.setStyleSheet("QGroupBox { margin-top: 24px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; font-weight: 900; font-size: 12px; color: #4c0c24; padding: 2px 10px; }")
        font_hist = QtGui.QFont()
        font_hist.setPointSize(12)
        font_hist.setBold(True)
        self.group_history_chart.setFont(font_hist)
        self.vbox_history_chart = QtWidgets.QVBoxLayout(self.group_history_chart)
        self.chart_view_history = QtWidgets.QWidget(parent=self.group_history_chart)
        self.chart_view_history.setObjectName("chart_view_history")
        self.chart_view_history.setSizePolicy(sizeExpand)
        self.vbox_history_chart.addWidget(self.chart_view_history)
        self.vbox_history.addWidget(self.group_history_chart)

        self.group_history_details = QtWidgets.QGroupBox(parent=self.tab_history)
        self.group_history_details.setTitle("History Details")
        self.group_history_details.setStyleSheet("QGroupBox { margin-top: 24px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; font-weight: 900; font-size: 12px; color: #4c0c24; padding: 2px 10px; }")
        self.group_history_details.setFont(font_hist)
        self.vbox_history_details = QtWidgets.QVBoxLayout(self.group_history_details)

        self.table_history = QtWidgets.QTableWidget(parent=self.group_history_details)
        self.table_history.setObjectName("table_history")
        self.table_history.setSizePolicy(sizeExpand)
        self.table_history.setColumnCount(4)
        self.table_history.setRowCount(0)
        for i in range(4):
            self.table_history.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())
        try:
            hdr_hist = self.table_history.horizontalHeader()
            hdr_hist.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        except Exception:
            pass
        try:
            self.table_history.verticalHeader().setVisible(False)
        except Exception:
            pass
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
        try:
            self.group_history_details.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding))
            self.table_history.setMinimumHeight(280)
        except Exception:
            pass
        self.vbox_history.setStretch(0, 1)
        self.vbox_history.setStretch(1, 2)

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

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_header_title.setText(_translate("MainWindow", "HOUSE PRICE PREDICTION - ADMIN"))