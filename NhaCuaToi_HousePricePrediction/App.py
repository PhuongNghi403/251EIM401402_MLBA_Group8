import os
import sys
import time
import pickle
from typing import Optional, Dict, List, Tuple

import numpy as np
import pandas as pd

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QTableWidgetItem,
    QVBoxLayout,
)

# Ensure we can import the generated UI class regardless of CWD
UI_DIR = os.path.join(os.path.dirname(__file__), "UI")
if UI_DIR not in sys.path:
    sys.path.append(UI_DIR)

from mainwindow_ui import Ui_MainWindow  # noqa: E402

# Matplotlib (QtAgg) for embedding charts
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

# Scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Core state
        self.df: Optional[pd.DataFrame] = None
        self.model_default = None
        self.models_cache: Dict[str, object] = {}
        self.history_df: pd.DataFrame = pd.DataFrame(
            columns=["Time", "Input Summary", "Predicted Price", "Model"]
        )

        # Training context
        self.feature_names: List[str] = []
        self.target_name: Optional[str] = None
        self.current_model_name: Optional[str] = None
        self.current_model_obj: Optional[object] = None

        # Matplotlib canvases
        self.canvas_compare, self.ax_compare = self._init_canvas_in(self.ui.chart_view_compare)
        self.canvas_history, self.ax_history = self._init_canvas_in(self.ui.chart_view_history)

        # Signal connections
        self._connect_signals()

        # Initial UI state
        self.ui.lbl_status_tab1.setText("Sẵn sàng.")

    # ---------- UI wiring helpers ----------
    def _init_canvas_in(self, host_widget: QtWidgets.QWidget) -> Tuple[FigureCanvas, object]:
        figure = Figure(figsize=(5, 3), tight_layout=True)
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

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

    # ---------- Tab 1: Dataset ----------
    def slot_pick_dataset(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn file CSV dữ liệu",
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
        self.ui.lbl_status_tab1.setText(f"Đã chọn: {file_path}")

    def slot_load_and_train(self):
        path = self.ui.combo_dataset.currentText().strip()
        if not path:
            self._error("Vui lòng chọn file CSV trước.")
            return

        train_rate = int(self.ui.spin_train_rate.value())
        if not os.path.isfile(path):
            self._error("Đường dẫn CSV không hợp lệ.")
            return

        try:
            self.df = pd.read_csv(path)
        except Exception as e:
            self._error(f"Lỗi đọc CSV: {e}")
            return

        self.helper_display_df_on_table(self.df, self.ui.table_dataset_preview)
        self.ui.lbl_status_tab1.setText("Đã tải dữ liệu. Bắt đầu huấn luyện LinearRegression...")

        model, metrics, results_df = self.run_training_process("LinearRegression", train_rate=train_rate)
        if model is None:
            return

        self.display_train_results(model, metrics, results_df)
        self.ui.tabWidget.setCurrentIndex(1)

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
            self._error("Chưa có dữ liệu. Hãy tải CSV ở Tab 1.")
            return None, {}, pd.DataFrame()

        df = self.df.copy() if df_train is None else pd.concat([df_train, df_test], axis=0)

        # Preferred schema
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
            # Fallback: use numeric columns
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(num_cols) < 2:
                self._error("Không đủ cột số để huấn luyện.")
                return None, {}, pd.DataFrame()
            target = num_cols[-1]
            feats = num_cols[:-1][:5]  # take up to 5 features
            X_all = df[feats]
            y_all = df[target].astype(float)

        self.feature_names = feats
        self.target_name = target

        if train_rate is None:
            train_rate = 80
        test_size = 1 - train_rate / 100.0
        X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=test_size, random_state=42)

        if model_name == "LinearRegression":
            model = LinearRegression()
        elif model_name == "RandomForest":
            model = RandomForestRegressor(n_estimators=200, random_state=42)
        elif model_name == "GradientBoosting":
            model = GradientBoostingRegressor(random_state=42)
        else:
            self._error(f"Model không hỗ trợ: {model_name}")
            return None, {}, pd.DataFrame()

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae = float(mean_absolute_error(y_test, y_pred))
        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        r2 = float(r2_score(y_test, y_pred))

        metrics = {"MAE": mae, "RMSE": rmse, "R2": r2}
        results_df = pd.DataFrame({"Giá trị thực": y_test.values, "Giá trị dự đoán": y_pred})

        self.models_cache[model_name] = model
        self.current_model_name = model_name
        self.current_model_obj = model

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
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Giá trị thực", "Giá trị dự đoán"])
        for r in range(len(results_df)):
            table.setItem(r, 0, QTableWidgetItem(str(results_df.iloc[r, 0])))
            table.setItem(r, 1, QTableWidgetItem(str(results_df.iloc[r, 1])))
        table.resizeColumnsToContents()

    def slot_save_model(self):
        if self.current_model_obj is None:
            self._error("Chưa có model để lưu. Hãy huấn luyện trước.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Lưu model", "", "Pickle (*.pkl);;Joblib (*.joblib)")
        if not path:
            return
        try:
            if path.endswith(".joblib"):
                import joblib  # lazy import
                joblib.dump(self.current_model_obj, path)
            else:
                with open(path, "wb") as f:
                    pickle.dump(self.current_model_obj, f)
            QMessageBox.information(self, "Thành công", f"Đã lưu model: {path}")
        except Exception as e:
            self._error(f"Lỗi lưu model: {e}")

    # ---------- Tab 3: Model Comparison ----------
    def slot_evaluate_all_models(self):
        if self.df is None:
            self._error("Chưa có dữ liệu. Hãy tải CSV ở Tab 1.")
            return

        self.ui.table_model_comparison.setRowCount(0)
        self.ui.combo_set_default_model.clear()
        self.ui.txt_model_metrics.setPlainText("Đang huấn luyện và đánh giá các model...")

        model_list = ["LinearRegression", "RandomForest", "GradientBoosting"]
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
        self.plot_comparison_chart(results_for_plot)
        self.ui.txt_model_metrics.setPlainText("Hoàn tất đánh giá các model.")

    def plot_comparison_chart(self, results: List[Tuple[str, float]]):
        self.ax_compare.clear()
        if not results:
            self.ax_compare.text(0.5, 0.5, "Không có dữ liệu để vẽ", ha="center", va="center")
        else:
            names = [r[0] for r in results]
            rmses = [r[1] for r in results]
            x = np.arange(len(names))
            self.ax_compare.bar(x, rmses, color="#5DADE2")
            self.ax_compare.set_xticks(x)
            self.ax_compare.set_xticklabels(names, rotation=0)
            self.ax_compare.set_ylabel("RMSE")
            self.ax_compare.set_title("So sánh RMSE giữu các Model")
            self.ax_compare.grid(axis="y", linestyle="--", alpha=0.4)
        self.canvas_compare.draw_idle()

    def slot_set_default_model(self):
        name = self.ui.combo_set_default_model.currentText().strip()
        if not name:
            return
        model = self.models_cache.get(name)
        if model is None:
            self._error("Model chưa được huấn luyện. Hãy đánh giá tất cả model trước.")
            return
        self.model_default = model
        QMessageBox.information(self, "Đã chọn", f"Model mặc định: {name}")

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
            self._error("Chưa chọn model mặc định ở Tab 3.")
            return

        vals = [
            self._get_float(self.ui.input_area_income),
            self._get_float(self.ui.input_house_age),
            self._get_float(self.ui.input_num_rooms),
            self._get_float(self.ui.input_num_bedrooms),
            self._get_float(self.ui.input_population),
        ]
        if any(v is None for v in vals):
            self._error("Vui lòng nhập đủ 5 giá trị số.")
            return

        if len(self.feature_names) != 5:
            self._error(
                "Model hiện tại không được huấn luyện với đúng 5 thuộc tính đầu vào. "
                "Hãy dùng dataset có các cột phù hợp (USA Housing schema) hoặc đánh giá lại."
            )
            return

        X_input = pd.DataFrame([vals], columns=self.feature_names)
        try:
            pred = float(self.model_default.predict(X_input)[0])
        except Exception as e:
            self._error(f"Lỗi dự đoán: {e}")
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
            self._error("Chưa có kết quả dự đoán để xuất.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Lưu báo cáo CSV", "", "CSV (*.csv)")
        if not path:
            return
        try:
            self.history_df.to_csv(path, index=False)
            QMessageBox.information(self, "Thành công", f"Đã xuất: {path}")
        except Exception as e:
            self._error(f"Lỗi xuất CSV: {e}")

    def _get_model_default_name(self) -> str:
        for name, obj in self.models_cache.items():
            if obj is self.model_default:
                return name
        return "Unknown"

    # ---------- Tab 5: History ----------
    def save_to_history(self, input_data: Dict[str, float], result: float, model_name: str):
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        summary = ", ".join(f"{k}={v}" for k, v in input_data.items())
        new_row = {"Time": ts, "Input Summary": summary, "Predicted Price": result, "Model": model_name}
        self.history_df = pd.concat([self.history_df, pd.DataFrame([new_row])], ignore_index=True)
        self.refresh_history_tab()

    def refresh_history_tab(self):
        table = self.ui.table_history
        df = self.history_df.copy()
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
        if self.history_df.empty:
            self.ax_history.text(0.5, 0.5, "Chưa có lịch sử", ha="center", va="center")
        else:
            y = self.history_df["Predicted Price"].astype(float).values
            x = np.arange(len(y))
            self.ax_history.plot(x, y, marker="o", color="#58D68D")
            self.ax_history.set_xlabel("Lần dự đoán")
            self.ax_history.set_ylabel("Giá dự đoán")
            self.ax_history.set_title("Xu hướng giá dự đoán theo thời gian")
            self.ax_history.grid(True, linestyle="--", alpha=0.4)
        self.canvas_history.draw_idle()

    def slot_delete_history(self):
        row = self.ui.table_history.currentRow()
        if row < 0 or row >= len(self.history_df):
            self._error("Hãy chọn một dòng để xóa.")
            return
        self.history_df = self.history_df.drop(self.history_df.index[row]).reset_index(drop=True)
        self.refresh_history_tab()

    def slot_clear_history(self):
        if self.history_df.empty:
            return
        confirm = QMessageBox.question(self, "Xác nhận", "Xóa toàn bộ lịch sử?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.history_df = pd.DataFrame(columns=["Time", "Input Summary", "Predicted Price", "Model"])
            self.refresh_history_tab()

    def slot_export_history(self):
        if self.history_df.empty:
            self._error("Lịch sử trống.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Xuất lịch sử CSV", "", "CSV (*.csv)")
        if not path:
            return
        try:
            self.history_df.to_csv(path, index=False)
            QMessageBox.information(self, "Thành công", f"Đã xuất: {path}")
        except Exception as e:
            self._error(f"Lỗi xuất CSV: {e}")

    # ---------- Common helpers ----------
    def _error(self, msg: str):
        QMessageBox.critical(self, "Lỗi", msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())