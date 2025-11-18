import os
import sys
import time
import pickle
from typing import Optional, Dict, List, Tuple

import numpy as np
import pandas as pd

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QTableWidgetItem,
    QVBoxLayout,
    QStyle,
    QDialog,
    QLineEdit,
    QComboBox,
    QDialogButtonBox,
    QLabel,
)

# Ensure we can import the generated UI class regardless of CWD
UI_DIR = os.path.join(os.path.dirname(__file__), "UI")
if UI_DIR not in sys.path:
    sys.path.append(UI_DIR)

from mainwindow_ui import Ui_MainWindow  # noqa: E402
from house_input_form import HouseInputForm  # noqa: E402

# Matplotlib (QtAgg) for embedding charts
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

# Scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

from SharedLogic import PredictionLogicMixin

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Đăng nhập")
        self.username_edit = QLineEdit(self)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_combo = QComboBox(self)
        self.role_combo.addItems(["customer", "admin"])
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, parent=self)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Tên người dùng"))
        layout.addWidget(self.username_edit)
        layout.addWidget(QLabel("Mật khẩu"))
        layout.addWidget(self.password_edit)
        layout.addWidget(QLabel("Vai trò"))
        layout.addWidget(self.role_combo)
        layout.addWidget(self.buttons)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.role_combo.currentTextChanged.connect(self._on_role_changed)
        self._on_role_changed(self.role_combo.currentText())

    @property
    def username(self) -> str:
        return self.username_edit.text().strip() or "guest"

    @property
    def role(self) -> str:
        return self.role_combo.currentText().strip() or "customer"

    def _on_role_changed(self, text: str):
        if text.strip().lower() == "customer":
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            if not self.password_edit.text():
                self.password_edit.setText("customer")
        else:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            if not self.password_edit.text():
                self.password_edit.setText("admin")


# class MainWindow: thêm kế thừa Mixin và khởi tạo mixin
class MainWindow(QMainWindow, Ui_MainWindow, PredictionLogicMixin):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        PredictionLogicMixin.__init__(self)

        # Clear default status text from UI design
        if hasattr(self.ui, "lbl_status_tab1"):
            self.ui.lbl_status_tab1.setText("")

        # Core state
        self.df: Optional[pd.DataFrame] = None
        self.model_default = None
        self.models_cache: Dict[str, object] = {}
        self.train_results_cache: Dict[str, Dict[str, object]] = {}
        self.history_df: pd.DataFrame = pd.DataFrame(
            columns=["Time", "Input Summary", "Predicted Price", "Model", "User"]
        )

        # Training context
        self.feature_names: List[str] = []
        self.target_name: Optional[str] = None
        self.current_model_name: Optional[str] = None
        self.current_model_obj: Optional[object] = None

        self.current_user: Optional[str] = None
        self.current_role: Optional[str] = None

        # Matplotlib canvases
        self.canvas_compare, self.ax_compare = self._init_canvas_in(self.ui.chart_view_compare)
        self.canvas_history, self.ax_history = self._init_canvas_in(self.ui.chart_view_history)
        self.compare_results_store: List[Tuple[str, float]] = []
        self.selected_compare_model: Optional[str] = None

        # Theme state + icons
        self._theme_mode = "light"
        self._apply_theme(self._theme_mode)
        self._apply_icons()

        # Signal connections
        self._connect_signals()

    # ---------- UI wiring helpers ----------
    def _init_canvas_in(self, host_widget: QtWidgets.QWidget) -> Tuple[FigureCanvas, object]:
        figure = Figure(figsize=(5, 3), tight_layout=True)
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        # Apply theme-dependent background
        if getattr(self, "_theme_mode", "light") == "dark":
            figure.set_facecolor("#221733")
            ax.set_facecolor("#2d2046")
        else:
            figure.set_facecolor("#f8e1f4")
            ax.set_facecolor("#ffffff")

        layout = host_widget.layout()
        if layout is None:
            layout = QVBoxLayout(host_widget)
            layout.setContentsMargins(6, 6, 6, 6)
        layout.addWidget(canvas)
        return canvas, ax

    def _connect_signals(self):
        self.ui.btn_pick_dataset.clicked.connect(self.slot_pick_dataset)
        self.ui.btn_load_and_train.clicked.connect(self.slot_load_and_train)

        self.ui.btn_save_model.clicked.connect(self.slot_save_model)

        self.ui.btn_evaluate_all_models.clicked.connect(self.slot_evaluate_all_models)
        self.ui.combo_set_default_model.currentTextChanged.connect(self.slot_set_default_model)

        self.ui.btn_predict.clicked.connect(self.slot_predict)
        self.ui.btn_export_report.clicked.connect(self.slot_export_report)

        self.ui.btn_delete_history.clicked.connect(self.slot_delete_history)
        self.ui.btn_clear_history.clicked.connect(self.slot_clear_history)
        self.ui.btn_export_history.clicked.connect(self.slot_export_history)

        # Theme toggle button (only if exists)
        if hasattr(self.ui, "btn_toggle_theme"):
            self.ui.btn_toggle_theme.clicked.connect(self._toggle_theme)

        if hasattr(self.ui, "btn_quick_evaluate"):
            self.ui.btn_quick_evaluate.clicked.connect(self.slot_quick_evaluate)
        if hasattr(self.ui, "btn_open_house_input_form"):
            self.ui.btn_open_house_input_form.clicked.connect(self.slot_open_house_input_form)
        if hasattr(self.ui, "combo_trained_models"):
            self.ui.combo_trained_models.currentTextChanged.connect(self.slot_select_trained_model)
        # Row selection for comparison table
        self.ui.table_model_comparison.itemSelectionChanged.connect(self.slot_compare_row_selected)
        # Visual feedback: selected row in yellow
        self.ui.table_model_comparison.setStyleSheet("QTableWidget::item:selected{background:#FFF59D;color:#2b2342;}")

    # --- Theme & Icons ---
    def _apply_theme(self, mode: str):
        if mode == "dark":
            palette = {
                "bg": "#1c1330",
                "pane": "#221733",
                "panel": "#2d2046",
                "text": "#ece7ff",
                "muted": "#cbbef5",
                "border": "#5b4f85",
                "btn": "#3a2c5e",
                "btn_hover": "#4a3976",
                "accent_bar": "#b68cff",
                "accent_line": "#93c0ff",
            }
            text_color = "#DDDDDD"
        else:
            palette = {
                "bg": "#f8e1f4",
                "pane": "#f8e1f4",
                "panel": "#f1d0f0",
                "text": "#2b2342",
                "muted": "#7b6f9e",
                "border": "#d6b6f5",
                "btn": "#f4e6fb",
                "btn_hover": "#ead6ff",
                "accent_bar": "#d491d3",
                "accent_line": "#a86fd6",
            }
            text_color = "#2b2342"

        style = f"""
            QMainWindow, QWidget#centralwidget {{
                background: {palette['bg']};
            }}
            QTabWidget::pane {{
                border: 1px solid {palette['border']};
                background: {palette['pane']};
                border-radius: 6px;
            }}
            QTabBar::tab {{
                background: {palette['btn']};
                color: {palette['text']};
                padding: 8px 16px;
                border: 1px solid {palette['border']};
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background: {palette['panel']};
                color: {palette['text']};
            }}
            QGroupBox {{
                background: {palette['panel']};
                border: 1px solid {palette['border']};
                border-radius: 8px;
                margin-top: 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 4px 8px;
                color: {palette['muted']};
            }}
            QPushButton {{
                background: {palette['btn']};
                color: {palette['text']};
                border: 1px solid {palette['border']};
                border-radius: 6px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background: {palette['btn_hover']};
            }}
            QTableWidget {{
                background: {'#2d2046' if mode=='dark' else '#ffffff'};
                color: {palette['text']};
                gridline-color: {palette['border']};
            }}
            QHeaderView::section {{
                background: {palette['btn']};
                color: {palette['text']};
                border: 1px solid {palette['border']};
                padding: 4px 8px;
            }}
            QLabel#lbl_prediction_result {{
                color: {palette['accent_line']};
                font-weight: 600;
            }}
            QSpinBox, QLineEdit, QComboBox {{
                background: {'#3a2c5e' if mode=='dark' else '#ffffff'};
                color: {palette['text']};
                border: 1px solid {palette['border']};
                border-radius: 4px;
                padding: 4px 6px;
            }}
        """
        self.setStyleSheet(style)
        self.compare_bar_color = palette["accent_bar"]
        self.history_line_color = palette["accent_line"]

        # Update current figures
        fig_bg_color = "#221733" if mode == "dark" else "#f8e1f4"
        ax_bg_color = "#2d2046" if mode == "dark" else "#ffffff"

        self.canvas_compare.figure.set_facecolor(fig_bg_color)
        self.ax_compare.set_facecolor(ax_bg_color)
        self.ax_compare.tick_params(colors=text_color, axis='x')
        self.ax_compare.tick_params(colors=text_color, axis='y')
        self.ax_compare.xaxis.label.set_color(text_color)
        self.ax_compare.yaxis.label.set_color(text_color)
        self.ax_compare.title.set_color(text_color)

        self.canvas_history.figure.set_facecolor(fig_bg_color)
        self.ax_history.set_facecolor(ax_bg_color)
        self.ax_history.tick_params(colors=text_color, axis='x')
        self.ax_history.tick_params(colors=text_color, axis='y')
        self.ax_history.xaxis.label.set_color(text_color)
        self.ax_history.yaxis.label.set_color(text_color)
        self.ax_history.title.set_color(text_color)

        self.canvas_compare.draw_idle()
        self.canvas_history.draw_idle()

    def _load_icon(self, name: str, fallback: QtWidgets.QStyle.StandardPixmap):
        icon_path = os.path.join(os.path.dirname(__file__), "UI", "icons", name)
        if os.path.isfile(icon_path):
            return QtGui.QIcon(icon_path)
        return self.style().standardIcon(fallback)

    def _apply_icons(self):
        s = self.style()
        # Tab 1
        self.ui.btn_pick_dataset.setIcon(self._load_icon("dataset.png", s.StandardPixmap.SP_DirOpenIcon))
        self.ui.btn_load_and_train.setIcon(self._load_icon("train.png", s.StandardPixmap.SP_MediaPlay))
        # Tab 2
        self.ui.btn_save_model.setIcon(self._load_icon("save.png", s.StandardPixmap.SP_DialogSaveButton))
        # Tab 3
        self.ui.btn_evaluate_all_models.setIcon(self._load_icon("compare.png", s.StandardPixmap.SP_BrowserReload))
        # Tab 4
        self.ui.btn_predict.setIcon(self._load_icon("predict.png", s.StandardPixmap.SP_ArrowForward))
        self.ui.btn_export_report.setIcon(self._load_icon("export.png", s.StandardPixmap.SP_DriveDVDIcon))
        # Tab 5
        self.ui.btn_delete_history.setIcon(self._load_icon("delete.png", s.StandardPixmap.SP_TrashIcon))
        self.ui.btn_clear_history.setIcon(self._load_icon("clear.png", s.StandardPixmap.SP_BrowserStop))
        self.ui.btn_export_history.setIcon(self._load_icon("export_history.png", s.StandardPixmap.SP_DriveHDIcon))

        # Tabs icons
        self.ui.tabWidget.setTabIcon(0, self._load_icon("tab_dataset.png", s.StandardPixmap.SP_DirIcon))
        self.ui.tabWidget.setTabIcon(1, self._load_icon("tab_train.png", s.StandardPixmap.SP_ComputerIcon))
        self.ui.tabWidget.setTabIcon(2, self._load_icon("tab_compare.png", s.StandardPixmap.SP_ArrowRight))
        self.ui.tabWidget.setTabIcon(3, self._load_icon("tab_predict.png", s.StandardPixmap.SP_ArrowForward))
        self.ui.tabWidget.setTabIcon(4, self._load_icon("tab_history.png", s.StandardPixmap.SP_FileIcon))

    def _toggle_theme(self):
        self._theme_mode = "dark" if self._theme_mode == "light" else "light"
        self._apply_theme(self._theme_mode)

    # ---------- Tab 1: Dataset ----------
    def slot_pick_dataset(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV data file",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )
        if not file_path:
            return
        idx = self.ui.combo_dataset.findText(file_path)
        if idx < 0:
            self.ui.combo_dataset.addItem(file_path)
            idx = self.ui.combo_dataset.count() - 1
        self.ui.combo_dataset.setCurrentIndex(idx)
        if hasattr(self.ui, "lbl_status_tab1"):
            self.ui.lbl_status_tab1.setText(f"Selected: {file_path}")

    def slot_load_and_train(self):
        if self.current_role == "customer":
            self._error("Chức năng chỉ dành cho admin.")
            return
        path = self.ui.combo_dataset.currentText().strip()
        if not path:
            self._error("Please select a CSV file first.")
            return
        train_rate = int(self.ui.spin_train_rate.value())
        if not os.path.isfile(path):
            self._error("Invalid CSV path.")
            return
        try:
            self.df = pd.read_csv(path)
        except Exception as e:
            self._error(f"CSV read error: {e}")
            return
        self.helper_display_df_on_table(self.df, self.ui.table_dataset_preview)
        if hasattr(self.ui, "lbl_status_tab1"):
            self.ui.lbl_status_tab1.setText("Data loaded. Starting LinearRegression training...")

        model, metrics, results_df = self.run_training_process("LinearRegression", train_rate=train_rate)
        if model is None:
            return

        # Update Tab 2 results, but stay on Tab 1 (no auto switch)
        self.display_train_results(model, metrics, results_df)

    def helper_display_df_on_table(self, df: pd.DataFrame, table: QtWidgets.QTableWidget):
        if df is None:
            return
        table.clear()
        table.setRowCount(df.shape[0])
        table.setColumnCount(df.shape[1])
        table.setHorizontalHeaderLabels([str(c) for c in df.columns])
        for r in range(df.shape[0]):
            for c in range(df.shape[1]):
                val = df.iat[r, c]
                table.setItem(r, c, QTableWidgetItem("" if pd.isna(val) else str(val)))
        table.resizeColumnsToContents()

    # ---------- Tab 2: Train Results ----------
    def run_training_process(
        self,
        model_name: str,
        df_train: Optional[pd.DataFrame] = None,
        df_test: Optional[pd.DataFrame] = None,
        train_rate: Optional[int] = None,
    ) -> Tuple[Optional[object], Dict[str, float], pd.DataFrame]:
        if self.df is None and df_train is None:
            self._error("No data. Please load a CSV in Tab 1.")
            return None, {}, pd.DataFrame()

        df = self.df.copy() if df_train is None else pd.concat([df_train, df_test], axis=0)

        preferred_feats = [
            "Avg Area Income",
            "Avg Area House Age",
            "Avg Area Number of Rooms",
            "Avg Area Number of Bedrooms",
            "Area Population",
        ]
        preferred_target = "Price"

        def normalize(s: str) -> str:
            return "".join(ch for ch in s.lower() if ch.isalnum())

        norm_cols = {normalize(c): c for c in df.columns}

        def find_col(name: str) -> Optional[str]:
            key = normalize(name)
            return norm_cols.get(key)

        feats = []
        for n in preferred_feats:
            col = find_col(n)
            if col is not None:
                feats.append(col)

        target = find_col(preferred_target)

        if len(feats) == 5 and target:
            X_all = df[feats].select_dtypes(include=[np.number])
            y_all = df[target].astype(float)
        else:
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(num_cols) < 2:
                self._error("Not enough numeric columns to train.")
                return None, {}, pd.DataFrame()
            target = num_cols[-1]
            feats = num_cols[:-1][:5]
            X_all = df[feats]
            y_all = df[target].astype(float)

        city_col = None
        city_col = city_col or find_col("City")
        city_all = df[city_col].astype(str) if city_col else pd.Series([""] * len(df), index=df.index)

        self.feature_names = feats
        self.target_name = target

        if train_rate is None:
            train_rate = 80
        test_size = 1 - train_rate / 100.0
        X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=test_size, random_state=42)
        city_test = city_all.loc[y_test.index]

        if model_name == "LinearRegression":
            model = LinearRegression()
        elif model_name == "RandomForest":
            model = RandomForestRegressor(n_estimators=200, random_state=42)
        elif model_name == "GradientBoosting":
            model = GradientBoostingRegressor(random_state=42)
        elif model_name == "XGBoost":
            model = XGBRegressor(random_state=42)
        elif model_name == "LightGBM":
            model = LGBMRegressor(random_state=42)
        else:
            self._error(f"Unsupported model: {model_name}")
            return None, {}, pd.DataFrame()

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae = float(mean_absolute_error(y_test, y_pred))
        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        r2 = float(r2_score(y_test, y_pred))

        metrics = {"MAE": mae, "RMSE": rmse, "R2": r2}
        results_df = pd.DataFrame({"City": city_test.values, "Giá trị thực": y_test.values, "Giá trị dự đoán": y_pred})

        self.models_cache[model_name] = model
        self.current_model_name = model_name
        self.current_model_obj = model
        self.train_results_cache[model_name] = {
            "metrics": metrics,
            "results_df": results_df,
            "feature_names": self.feature_names.copy(),
            "target": self.target_name,
        }
        self._populate_trained_models_combo()

        return model, metrics, results_df

    def display_train_results(self, model: object, metrics: Dict[str, float], results_df: pd.DataFrame):
        lines = [
            f"Model: {self.current_model_name}",
            f"Features: {', '.join(self.feature_names)}",
            f"Target: {self.target_name}",
            f"MAE: {metrics.get('MAE', float('nan')):,.4f}",
            f"RMSE: {metrics.get('RMSE', float('nan')):,.4f}",
            f"R²: {metrics.get('R2', float('nan')):,.4f}",
        ]
        self.ui.txt_model_metrics.setPlainText("\n".join(lines))

        table = self.ui.table_train_results
        table.clearContents()
        table.setRowCount(len(results_df))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["City", "Giá trị thực", "Giá trị dự đoán"])
        for r in range(len(results_df)):
            table.setItem(r, 0, QTableWidgetItem(str(results_df.iloc[r, 0])))
            table.setItem(r, 1, QTableWidgetItem(str(results_df.iloc[r, 1])))
            table.setItem(r, 2, QTableWidgetItem(str(results_df.iloc[r, 2])))
        table.resizeColumnsToContents()

    # ---------- Tab 3: Model Comparison ----------
    def slot_evaluate_all_models(self):
        if self.current_role == "customer":
            self._error("Chức năng chỉ dành cho admin.")
            return
        if self.df is None:
            self._error("No data. Please load a CSV in Tab 1.")
            return

        self.ui.table_model_comparison.setRowCount(0)
        self.ui.combo_set_default_model.clear()
        self.ui.txt_model_metrics.setPlainText("Training and evaluating models...")

        self.ui.table_model_comparison.setColumnCount(4)
        self.ui.table_model_comparison.setHorizontalHeaderLabels(["Model", "MAE", "RMSE", "R²"])

        model_list = ["LinearRegression", "RandomForest", "GradientBoosting", "XGBoost", "LightGBM"]
        results_for_plot: List[Tuple[str, float]] = []

        train_rate = int(self.ui.spin_train_rate.value())

        for name in model_list:
            model, metrics, _ = self.run_training_process(name, train_rate=train_rate)
            if model is None:
                continue
            row = self.ui.table_model_comparison.rowCount()
            self.ui.table_model_comparison.insertRow(row)
            self.ui.table_model_comparison.setItem(row, 0, QTableWidgetItem(name))
            self.ui.table_model_comparison.setItem(row, 1, QTableWidgetItem(f"{metrics['MAE']:.4f}"))
            self.ui.table_model_comparison.setItem(row, 2, QTableWidgetItem(f"{metrics['RMSE']:.4f}"))
            self.ui.table_model_comparison.setItem(row, 3, QTableWidgetItem(f"{metrics['R2']:.4f}"))
            results_for_plot.append((name, metrics["RMSE"]))
            if self.ui.combo_set_default_model.findText(name) < 0:
                self.ui.combo_set_default_model.addItem(name)

        self.ui.table_model_comparison.resizeColumnsToContents()
        self.compare_results_store = results_for_plot
        self.plot_comparison_chart(results_for_plot, selected_name=self.selected_compare_model)
        self.ui.txt_model_metrics.setPlainText("Completed model evaluation.")
        self._populate_trained_models_combo()

    def plot_comparison_chart(self, results: List[Tuple[str, float]], selected_name: Optional[str] = None):
        self.ax_compare.clear()
        text_color = "#DDDDDD" if self._theme_mode == "dark" else "#2b2342"
        if not results:
            self.ax_compare.text(0.5, 0.5, "No data to plot", ha="center", va="center", color=text_color)
        else:
            names = [r[0] for r in results]
            rmses = [r[1] for r in results]
            x = np.arange(len(names))
            colors = [("#FFC107" if selected_name and n == selected_name else self.compare_bar_color) for n in names]
            self.ax_compare.bar(x, rmses, color=colors)
            self.ax_compare.set_xticks(x)
            self.ax_compare.set_xticklabels(names, rotation=0, color=text_color)
            self.ax_compare.set_ylabel("RMSE")
            title = "RMSE comparison across models"
            if selected_name:
                title += f" (Selected: {selected_name})"
            self.ax_compare.set_title(title)
            self.ax_compare.grid(axis="y", linestyle="--", alpha=0.4)
        self.canvas_compare.draw_idle()

    def slot_compare_row_selected(self):
        rows = self.ui.table_model_comparison.selectionModel().selectedRows()
        if not rows:
            self.selected_compare_model = None
            self.plot_comparison_chart(self.compare_results_store, selected_name=None)
            return
        row = rows[0].row()
        item = self.ui.table_model_comparison.item(row, 0)
        if not item:
            return
        name = item.text().strip()
        if not name:
            return
        self.selected_compare_model = name
        self.plot_comparison_chart(self.compare_results_store, selected_name=name)

    def slot_set_default_model(self):
        name = self.ui.combo_set_default_model.currentText().strip()
        if not name:
            return
        model = self.models_cache.get(name)
        if model is None:
            self._error("Model not trained yet. Please evaluate all models first.")
            return
        self.model_default = model
        QMessageBox.information(self, "Selected", f"Default model: {name}")
        try:
            self.update_current_model_info()
        except Exception:
            pass

    # ---------- Tab 4: Prediction ----------
    def _get_float(self, line_edit: QtWidgets.QLineEdit) -> Optional[float]:
        text = line_edit.text().strip()
        if not text:
            return None
        try:
            return float(text)
        except Exception:
            return None

    def slot_predict(self):
        if self.model_default is None:
            self._error("No default model selected in Tab 3.")
            return

        vals = [
            self._get_float(self.ui.input_area_income),
            self._get_float(self.ui.input_house_age),
            self._get_float(self.ui.input_num_rooms),
            self._get_float(self.ui.input_num_bedrooms),
            self._get_float(self.ui.input_population),
        ]
        if any(v is None for v in vals):
            self._error("Please enter all 5 numeric values.")
            return
        if len(self.feature_names) != 5:
            self._error(
                "The current model was not trained with exactly 5 input features. "
                "Use a dataset with the USA Housing schema or re-evaluate."
            )
            return

        X_input = pd.DataFrame([vals], columns=self.feature_names)
        try:
            pred = float(self.model_default.predict(X_input)[0])
        except Exception as e:
            self._error(f"Prediction error: {e}")
            return

        self.ui.lbl_prediction_result.setText(f"{pred:,.2f}")
        self.save_to_history(
            input_data=dict(
                AvgAreaIncome=vals[0],
                AvgAreaHouseAge=vals[1],
                AvgAreaNumRooms=vals[2],
                AvgAreaNumBedrooms=vals[3],
                AreaPopulation=vals[4],
            ),
            result=pred,
            model_name=self._get_model_default_name(),
        )

    def slot_export_report(self):
        if self.history_df.empty:
            self._error("No prediction result to export.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save report CSV", "", "CSV (*.csv)")
        if not path:
            return
        try:
            self.history_df.tail(1).to_csv(path, index=False)
            QMessageBox.information(self, "Success", f"Exported: {path}")
        except Exception as e:
            self._error(f"CSV export error: {e}")

    def _populate_trained_models_combo(self):
        if not hasattr(self.ui, "combo_trained_models"):
            return
        existing = set(self._iter_combo_items(self.ui.combo_trained_models))
        for name in self.train_results_cache.keys():
            if name not in existing:
                self.ui.combo_trained_models.addItem(name)
        # Ensure current selection reflects latest trained model
        if self.current_model_name:
            idx = self.ui.combo_trained_models.findText(self.current_model_name)
            if idx >= 0:
                self.ui.combo_trained_models.setCurrentIndex(idx)

    def _iter_combo_items(self, combo: QtWidgets.QComboBox):
        return [combo.itemText(i) for i in range(combo.count())]

    def slot_select_trained_model(self):
        name = self.ui.combo_trained_models.currentText().strip()
        if not name:
            return
        cached = self.train_results_cache.get(name)
        if not cached:
            return
        self.current_model_name = name
        self.feature_names = list(cached.get("feature_names", []))
        self.target_name = cached.get("target")
        metrics = cached.get("metrics", {})
        results_df = cached.get("results_df")
        if isinstance(results_df, pd.DataFrame):
            self.display_train_results(self.models_cache.get(name), metrics, results_df)

    def _get_model_default_name(self) -> str:
        for name, obj in self.models_cache.items():
            if obj is self.model_default:
                return name
        return "Unknown"

    # ---------- Tab 5: History ----------
    def save_to_history(self, input_data: Dict[str, float], result: float, model_name: str):
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        summary = ", ".join(f"{k}={v}" for k, v in input_data.items())
        new_row = {"Time": ts, "Input Summary": summary, "Predicted Price": result, "Model": model_name, "User": self.current_user or ""}
        self.history_df = pd.concat([self.history_df, pd.DataFrame([new_row])], ignore_index=True)
        self.refresh_history_tab()

    def refresh_history_tab(self):
        table = self.ui.table_history
        df = self.get_visible_history_df()
        table.clearContents()
        table.setRowCount(len(df))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Time", "Input Summary", "Predicted Price", "Model"])
        for r in range(len(df)):
            for c, col in enumerate(["Time", "Input Summary", "Predicted Price", "Model"]):
                table.setItem(r, c, QTableWidgetItem(str(df.iloc[r][col])))
        table.resizeColumnsToContents()
        self.plot_history_trend()

    def plot_history_trend(self):
        self.ax_history.clear()
        text_color = "#DDDDDD" if self._theme_mode == "dark" else "#2b2342"
        if self.history_df.empty:
            self.ax_history.text(0.5, 0.5, "No history yet", ha="center", va="center", color=text_color)
        else:
            y = self.history_df["Predicted Price"].astype(float).values
            x = np.arange(len(y))
            self.ax_history.plot(x, y, marker="o", color=self.history_line_color)
            self.ax_history.set_xlabel("Prediction #")
            self.ax_history.set_ylabel("Predicted Price")
            self.ax_history.set_title("Predicted price trend over time")
            self.ax_history.grid(True, linestyle="--", alpha=0.4)
        self.canvas_history.draw_idle()

    def slot_delete_history(self):
        if self.current_role == "customer":
            self._error("Chức năng chỉ dành cho admin.")
            return
        row = self.ui.table_history.currentRow()
        if row < 0 or row >= len(self.history_df):
            self._error("Please select a row to delete.")
            return
        self.history_df = self.history_df.drop(self.history_df.index[row]).reset_index(drop=True)
        self.refresh_history_tab()

    def slot_clear_history(self):
        if self.current_role == "customer":
            self._error("Chức năng chỉ dành cho admin.")
            return
        if self.history_df.empty:
            return
        confirm = QMessageBox.question(self, "Confirm", "Clear entire history?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.history_df = pd.DataFrame(columns=["Time", "Input Summary", "Predicted Price", "Model", "User"])
            self.refresh_history_tab()

    def slot_export_history(self):
        if self.history_df.empty:
            self._error("History is empty.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export history CSV", "", "CSV (*.csv)")
        if not path:
            return
        try:
            self.history_df.to_csv(path, index=False)
            QMessageBox.information(self, "Success", f"Exported: {path}")
        except Exception as e:
            self._error(f"CSV export error: {e}")

    # ---------- Common helpers ----------
    def _error(self, msg: str):
        QMessageBox.critical(self, "Error", msg)

    def _show_login_and_apply_role(self):
        dlg = LoginDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.current_user = dlg.username
            self.current_role = dlg.role

            # Nếu là customer: mở giao diện riêng, đóng MainWindow để tránh conflict
            if self.current_role == "customer":
                from customer_app import CustomerWindow
                cust = CustomerWindow(username=self.current_user)

                # Đồng bộ theme và chia sẻ lịch sử
                try:
                    cust._theme_mode = getattr(self, "_theme_mode", "light")
                    cust._apply_theme(cust._theme_mode)
                except Exception:
                    pass
                try:
                    cust.history_df = self.history_df
                except Exception:
                    pass

                cust.show()
                self.close()
                return

            # Admin: giữ nguyên 5 tab như cũ
            self.apply_role_permissions()
            try:
                self.update_current_model_info()
            except Exception:
                pass
        else:
            sys.exit(0)

    def _ensure_model_for_customer(self) -> bool:
        if self.model_default is not None:
            return True
        try:
            from NhaCuaToi_HousePricePrediction.FileUtils import FileUtils
            pkl_path = os.path.join(os.path.dirname(__file__), "data", "SaveModelTest1.pkl")
            if os.path.isfile(pkl_path):
                m = FileUtils.loadmodel(pkl_path)
                if m is not None:
                    self.model_default = m
                    if not self.feature_names or len(self.feature_names) != 5:
                        self.feature_names = [
                            "Avg Area Income",
                            "Avg Area House Age",
                            "Avg Area Number of Rooms",
                            "Avg Area Number of Bedrooms",
                            "Area Population",
                        ]
                    return True
        except Exception:
            pass
        try:
            csv_path = os.path.join(os.path.dirname(__file__), "data", "SuperCleaned_vietnam_housing_dataset.csv")
            if os.path.isfile(csv_path):
                self.df = pd.read_csv(csv_path)
                model, metrics, _ = self.run_training_process("LinearRegression", train_rate=int(self.ui.spin_train_rate.value()))
                if model is not None:
                    self.model_default = model
                    return True
        except Exception:
            pass
        return False

    def apply_role_permissions(self):
        if self.current_role == "customer":
            self.ui.tabWidget.setTabEnabled(0, False)
            self.ui.tabWidget.setTabEnabled(1, False)
            self.ui.tabWidget.setTabEnabled(2, False)
            self.ui.btn_load_and_train.setEnabled(False)
            self.ui.btn_save_model.setEnabled(False)
            self.ui.btn_evaluate_all_models.setEnabled(False)
            self.ui.combo_set_default_model.setEnabled(False)
            self.ui.btn_delete_history.setEnabled(False)
            self.ui.btn_clear_history.setEnabled(False)
            self.ui.btn_export_history.setEnabled(True)
            if hasattr(self.ui, "btn_open_house_input_form"):
                self.ui.btn_open_house_input_form.setEnabled(True)
        else:
            self.ui.tabWidget.setTabEnabled(0, True)
            self.ui.tabWidget.setTabEnabled(1, True)
            self.ui.tabWidget.setTabEnabled(2, True)
            self.ui.btn_load_and_train.setEnabled(True)
            self.ui.btn_save_model.setEnabled(True)
            self.ui.btn_evaluate_all_models.setEnabled(True)
            self.ui.combo_set_default_model.setEnabled(True)
            self.ui.btn_delete_history.setEnabled(True)
            self.ui.btn_clear_history.setEnabled(True)
            self.ui.btn_export_history.setEnabled(True)
            if hasattr(self.ui, "btn_open_house_input_form"):
                self.ui.btn_open_house_input_form.setEnabled(True)

    def get_visible_history_df(self) -> pd.DataFrame:
        if self.current_role == "customer" and self.current_user:
            return self.history_df[self.history_df["User"] == self.current_user].copy()
        return self.history_df.copy()

    def update_current_model_info(self):
        name = self._get_model_default_name()
        if hasattr(self.ui, "lbl_current_model"):
            self.ui.lbl_current_model.setText(f"Model: {name}")
        mae_text = "MAE: N/A"
        rmse_text = "RMSE: N/A"
        try:
            if self.model_default is not None and self.df is not None:
                req_names = list(getattr(self.model_default, "feature_names_in_", []))
                target = self.target_name if self.target_name else ("Price" if "Price" in self.df.columns else None)
                if req_names and target and all(col in self.df.columns for col in req_names):
                    X_all = self.df[req_names].select_dtypes(include=[np.number])
                    y_all = self.df[target].astype(float)
                    if len(X_all) > 5:
                        X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.2, random_state=42)
                        y_pred = self.model_default.predict(X_test)
                        mae_text = f"MAE: {mean_absolute_error(y_test, y_pred):,.4f}"
                        rmse_text = f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):,.4f}"
        except Exception:
            pass
        if hasattr(self.ui, "lbl_current_model_mae"):
            self.ui.lbl_current_model_mae.setText(mae_text)
        if hasattr(self.ui, "lbl_current_model_rmse"):
            self.ui.lbl_current_model_rmse.setText(rmse_text)

    def slot_open_house_input_form(self):
        if self.model_default is None:
            self._ensure_model_for_customer()
        try:
            self.update_current_model_info()
        except Exception:
            pass
        dlg = HouseInputForm(self)
        dlg.exec()

    def slot_quick_evaluate(self):
        self._ensure_model_for_customer()
        if self.model_default is None:
            self._error("Chưa có model để đánh giá.")
            return
        if self.df is None:
            try:
                csv_path = os.path.join(os.path.dirname(__file__), "data", "SuperCleaned_vietnam_housing_dataset.csv")
                if os.path.isfile(csv_path):
                    self.df = pd.read_csv(csv_path)
                else:
                    self._error("Không tìm thấy CSV để đánh giá.")
                    return
            except Exception as e:
                self._error(f"Lỗi đọc CSV: {e}")
                return
        try:
            req_names = list(getattr(self.model_default, "feature_names_in_", []))
            if not req_names:
                req_names = ["Area", "Bathrooms", "Bedrooms", "Floors", "Frontage"]
            if not all(col in self.df.columns for col in req_names):
                self._error("CSV không có đủ cột để đánh giá.")
                return
            target = "Price" if "Price" in self.df.columns else self.target_name
            if not target or target not in self.df.columns:
                self._error("Không tìm thấy cột Price trong CSV.")
                return
            X_all = self.df[req_names].select_dtypes(include=[np.number])
            y_all = self.df[target].astype(float)
            if len(X_all) < 10:
                self._error("Dữ liệu quá ít để đánh giá.")
                return
            X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.2, random_state=42)
            y_pred = self.model_default.predict(X_test)
            mae_val = mean_absolute_error(y_test, y_pred)
            rmse_val = np.sqrt(mean_squared_error(y_test, y_pred))
            if hasattr(self.ui, "lbl_current_model_mae"):
                self.ui.lbl_current_model_mae.setText(f"MAE: {mae_val:,.4f}")
            if hasattr(self.ui, "lbl_current_model_rmse"):
                self.ui.lbl_current_model_rmse.setText(f"RMSE: {rmse_val:,.4f}")
            if hasattr(self.ui, "lbl_current_model"):
                self.ui.lbl_current_model.setText(f"Model: {self._get_model_default_name()}")
        except Exception as e:
            self._error(f"Lỗi đánh giá: {e}")

    def slot_save_model(self):
        # Ensure there is a model trained and displayed in Tab 2
        if self.current_model_obj is None or self.current_model_name is None:
            self._error("Chưa có model để lưu. Hãy huấn luyện trước ở Tab 1 hoặc đánh giá ở Tab 3.")
            return

        # Suggest a default filename in the project's data folder
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        default_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(default_dir, exist_ok=True)
        default_name = f"{self.current_model_name}_{timestamp}.pkl"
        default_path = os.path.join(default_dir, default_name)

        # Ask user where to save
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Lưu model hiện tại",
            default_path,
            "Pickle Files (*.pkl);;All Files (*)",
        )
        if not path:
            return

        # Ensure .pkl extension
        if not path.lower().endswith(".pkl"):
            path = f"{path}.pkl"

        # Save using pickle
        try:
            with open(path, "wb") as f:
                pickle.dump(self.current_model_obj, f)
            QMessageBox.information(self, "Thành công", f"Đã lưu model: {path}")
        except Exception as e:
            self._error(f"Lỗi lưu model: {e}")