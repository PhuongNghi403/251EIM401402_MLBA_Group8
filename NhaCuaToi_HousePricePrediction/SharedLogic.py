from typing import Optional, Dict, Tuple, List
import time
import numpy as np
import pandas as pd
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem, QVBoxLayout, QFileDialog, QMessageBox
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class PredictionLogicMixin:
    def __init__(self):
        if not hasattr(self, "_theme_mode"):
            self._theme_mode = "dark"  # dùng tông tối giống ảnh bạn
        # Khởi tạo canvas lịch sử nếu có widget
        if hasattr(self, "ui") and hasattr(self.ui, "chart_view_history"):
            self.canvas_history, self.ax_history = self._init_canvas_in(self.ui.chart_view_history)

    def _init_canvas_in(self, host_widget: QtWidgets.QWidget) -> Tuple[FigureCanvas, object]:
        figure = Figure(figsize=(5, 3), tight_layout=True)
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

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

    def _get_float(self, line_edit: QtWidgets.QLineEdit) -> Optional[float]:
        text = line_edit.text().strip()
        if not text:
            return None
        try:
            return float(text)
        except Exception:
            return None

    def _get_model_default_name(self) -> str:
        if hasattr(self, "models_cache") and hasattr(self, "model_default"):
            for name, obj in self.models_cache.items():
                if obj is self.model_default:
                    return name
        return "Unknown"

    def get_visible_history_df(self) -> pd.DataFrame:
        role = getattr(self, "current_role", None)
        user = getattr(self, "current_user", None)
        if role == "customer" and user:
            return self.history_df[self.history_df["User"] == user].copy()
        return self.history_df.copy()

    def slot_predict(self):
        # Đảm bảo có model mặc định
        if getattr(self, "model_default", None) is None:
            if hasattr(self, "_ensure_model_for_customer"):
                self._ensure_model_for_customer()
        if getattr(self, "model_default", None) is None:
            self._error("No default model available. Please train or load a model.")
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

        feature_names = getattr(self, "feature_names", [])
        if not feature_names or len(feature_names) != 5:
            # fallback tên cột chuẩn USA Housing nếu thiếu
            feature_names = [
                "Avg Area Income",
                "Avg Area House Age",
                "Avg Area Number of Rooms",
                "Avg Area Number of Bedrooms",
                "Area Population",
            ]

        X_input = pd.DataFrame([vals], columns=feature_names)
        try:
            pred = float(self.model_default.predict(X_input)[0])
        except Exception as e:
            self._error(f"Prediction error: {e}")
            return

        if hasattr(self.ui, "lbl_prediction_result"):
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
        path, _ = QFileDialog.getSaveFileName(getattr(self, "self", None) or self, "Save report CSV", "", "CSV (*.csv)")
        if not path:
            return
        try:
            self.history_df.tail(1).to_csv(path, index=False)
            QMessageBox.information(getattr(self, "self", None) or self, "Success", f"Exported: {path}")
        except Exception as e:
            self._error(f"CSV export error: {e}")

    def save_to_history(self, input_data: Dict[str, float], result: float, model_name: str):
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        summary = ", ".join(f"{k}={v}" for k, v in input_data.items())
        user = getattr(self, "current_user", "") or ""
        new_row = {"Time": ts, "Input Summary": summary, "Predicted Price": result, "Model": model_name, "User": user}
        self.history_df = pd.concat([self.history_df, pd.DataFrame([new_row])], ignore_index=True)
        self.refresh_history_tab()

    def refresh_history_tab(self):
        if not hasattr(self.ui, "table_history"):
            return
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
        if not hasattr(self, "ax_history") or not hasattr(self, "canvas_history"):
            return
        self.ax_history.clear()
        text_color = "#DDDDDD" if getattr(self, "_theme_mode", "light") == "dark" else "#2b2342"
        if self.history_df.empty:
            self.ax_history.text(0.5, 0.5, "No history yet", ha="center", va="center", color=text_color)
        else:
            y = self.history_df["Predicted Price"].astype(float).values
            x = np.arange(len(y))
            self.ax_history.plot(x, y, marker="o", color=getattr(self, "history_line_color", "#a86fd6"))
            self.ax_history.set_xlabel("Prediction #")
            self.ax_history.set_ylabel("Predicted Price")
            self.ax_history.set_title("Predicted price trend over time")
            self.ax_history.grid(True, linestyle="--", alpha=0.4)
        self.canvas_history.draw_idle()

    def _apply_theme(self, mode: str):
        # Palette và stylesheet giống MainWindow
        if mode == "dark":
            palette = {
                "bg": "#1c1330", "pane": "#221733", "panel": "#2d2046",
                "text": "#ece7ff", "muted": "#cbbef5", "border": "#5b4f85",
                "btn": "#3a2c5e", "btn_hover": "#4a3976",
                "accent_bar": "#b68cff", "accent_line": "#93c0ff",
            }
            text_color = "#DDDDDD"
        else:
            palette = {
                "bg": "#f8e1f4", "pane": "#f8e1f4", "panel": "#f1d0f0",
                "text": "#2b2342", "muted": "#7b6f9e", "border": "#d6b6f5",
                "btn": "#f4e6fb", "btn_hover": "#ead6ff",
                "accent_bar": "#d491d3", "accent_line": "#a86fd6",
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
        try:
            # CustomerWindow/ MainWindow đều có self.setStyleSheet
            self.setStyleSheet(style)
        except Exception:
            pass
        # Cập nhật màu biểu đồ lịch sử nếu đã khởi tạo
        if hasattr(self, "canvas_history") and hasattr(self, "ax_history"):
            fig_bg_color = "#221733" if mode == "dark" else "#f8e1f4"
            ax_bg_color = "#2d2046" if mode == "dark" else "#ffffff"
            self.canvas_history.figure.set_facecolor(fig_bg_color)
            self.ax_history.set_facecolor(ax_bg_color)
            self.ax_history.tick_params(colors=text_color, axis='x')
            self.ax_history.tick_params(colors=text_color, axis='y')
            self.ax_history.xaxis.label.set_color(text_color)
            self.ax_history.yaxis.label.set_color(text_color)
            self.ax_history.title.set_color(text_color)
            self.canvas_history.draw_idle()

    def slot_delete_history(self):
        if not hasattr(self.ui, "table_history") or self.history_df.empty:
            return
        row = self.ui.table_history.currentRow()
        df = self.get_visible_history_df()
        if row < 0 or row >= len(df):
            self._error("Please select a row to delete.")
            return
        sel = df.iloc[row]
        mask = (
            (self.history_df["Time"] == sel["Time"]) &
            (self.history_df["Input Summary"] == sel["Input Summary"]) &
            (self.history_df["Predicted Price"] == sel["Predicted Price"]) &
            (self.history_df["Model"] == sel["Model"])
        )
        idxs = list(self.history_df.index[mask])
        if not idxs:
            self._error("Cannot find selected row in full history.")
            return
        self.history_df = self.history_df.drop(idxs[0]).reset_index(drop=True)
        self.refresh_history_tab()

    def slot_clear_history(self):
        if self.history_df.empty:
            return
        role = getattr(self, "current_role", None)
        user = getattr(self, "current_user", None)
        if role == "customer" and user:
            confirm = QMessageBox.question(getattr(self, "self", None) or self, "Confirm", "Clear your history?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm != QMessageBox.StandardButton.Yes:
                return
            self.history_df = self.history_df[self.history_df["User"] != user].reset_index(drop=True)
        else:
            confirm = QMessageBox.question(getattr(self, "self", None) or self, "Confirm", "Clear entire history?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm != QMessageBox.StandardButton.Yes:
                return
            self.history_df = pd.DataFrame(columns=["Time", "Input Summary", "Predicted Price", "Model", "User"])
        self.refresh_history_tab()

    def slot_export_history(self):
        df = self.get_visible_history_df()
        if df.empty:
            self._error("History is empty.")
            return
        path, _ = QFileDialog.getSaveFileName(getattr(self, "self", None) or self, "Export history CSV", "", "CSV (*.csv)")
        if not path:
            return
        try:
            df.to_csv(path, index=False)
            QMessageBox.information(getattr(self, "self", None) or self, "Success", f"Exported: {path}")
        except Exception as e:
            self._error(f"CSV export error: {e}")