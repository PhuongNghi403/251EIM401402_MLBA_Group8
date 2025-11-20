from PyQt6 import QtWidgets, QtGui, QtCore
import sys
import subprocess
import pandas as pd
import numpy as np
from PyQt6.QtWidgets import QMainWindow, QMessageBox
import os
import importlib.util
import webbrowser
import socket
import urllib.request
from UI.customer_home_ui import Ui_CustomerHome
from SharedLogic import PredictionLogicMixin
from UI.house_input_form import HouseInputForm
import threading
import time

class CustomerWindow(QMainWindow, Ui_CustomerHome, PredictionLogicMixin):
    def __init__(self, username: str = "customer"):
        super().__init__()
        self.ui = Ui_CustomerHome()
        self.ui.setupUi(self)
        try:
            self.ui.tabWidget.setCurrentIndex(0)
        except Exception:
            pass
        try:
            QtCore.QTimer.singleShot(0, lambda: self.ui.tabWidget.setCurrentIndex(0))
        except Exception:
            pass
        try:
            self._apply_icons()
        except Exception:
            pass
        try:
            self._apply_tab_titles_plain()
        except Exception:
            pass
        # Khởi tạo dữ liệu lịch sử trước khi mixin dùng
        self.history_df = pd.DataFrame(columns=["Time", "Input Summary", "Predicted Price", "Model", "User"])
        PredictionLogicMixin.__init__(self)
        self.current_user = username
        self.current_role = "customer"
        

        # Set icon cho btn_logout bằng QStyle
        style = self.style()
        self.ui.btn_logout.setIcon(style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_TitleBarCloseButton))

        # Kết nối nút nếu tồn tại (đã bỏ khung Results & Actions)
        if hasattr(self.ui, "btn_predict"):
            self.ui.btn_predict.clicked.connect(self.slot_predict)
        if hasattr(self.ui, "btn_export_report"):
            self.ui.btn_export_report.clicked.connect(self.slot_export_report)
        self.ui.btn_logout.clicked.connect(self._handle_logout)
        if hasattr(self.ui, "btn_start_chatbot"):
            self.ui.btn_start_chatbot.clicked.connect(self._start_chatbot_server)
        # Inline house input form embedded in predict tab
        if hasattr(self.ui, "widget_house_inline_container"):
            try:
                self.inline_house_form = HouseInputForm(self)
                self.inline_house_form.setModal(False)
                self.inline_house_form.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding))
                # embed the dialog as a child widget inside the container
                layout = self.ui.widget_house_inline_container.layout()
                if layout is None:
                    layout = QtWidgets.QVBoxLayout(self.ui.widget_house_inline_container)
                    layout.setContentsMargins(0, 0, 0, 0)
                self.ui.widget_house_inline_container.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding))
                layout.addWidget(self.inline_house_form)
            except Exception:
                pass
        # Web view cho chatbot nếu có
        self._chatbot_webview = None
        try:
            from PyQt6.QtWebEngineWidgets import QWebEngineView
            if hasattr(self.ui, "widget_chatbot_web"):
                self._chatbot_webview = QWebEngineView(self.ui.widget_chatbot_web)
                layout_web = self.ui.widget_chatbot_web.layout()
                if layout_web is None:
                    layout_web = QtWidgets.QVBoxLayout(self.ui.widget_chatbot_web)
                    layout_web.setContentsMargins(0, 0, 0, 0)
                layout_web.addWidget(self._chatbot_webview)
        except Exception:
            pass
        if hasattr(self.ui, "btn_toggle_theme"):
            self.ui.btn_toggle_theme.clicked.connect(self._toggle_theme)
        # Canvas bản đồ inline
        if hasattr(self.ui, "chart_view_city_map"):
            self.canvas_city_map, self.ax_city_map = self._init_canvas_in(self.ui.chart_view_city_map)
        if hasattr(self.ui, "chart_view_price_trend"):
            self.canvas_price_trend, self.ax_price_trend = self._init_canvas_in(self.ui.chart_view_price_trend)
            try:
                self.ui.chart_view_price_trend.setVisible(False)
            except Exception:
                pass
        if hasattr(self.ui, "chart_view_price_breakdown"):
            self.canvas_price_breakdown, self.ax_price_breakdown = self._init_canvas_in(self.ui.chart_view_price_breakdown)
            try:
                self.ui.chart_view_price_breakdown.setVisible(False)
            except Exception:
                pass
        # Render khi chuyển sang tab Bản đồ
        self.ui.tabWidget.currentChanged.connect(self._on_tab_changed)

        # Lịch sử
        self.ui.btn_delete_history.clicked.connect(self.slot_delete_history)
        self.ui.btn_clear_history.clicked.connect(self.slot_clear_history)
        self.ui.btn_export_history.clicked.connect(self.slot_export_history)

        # Áp dụng theme và chuẩn hóa bảng
        self._apply_theme(getattr(self, "_theme_mode", "dark"))
        self.ui.table_history.setColumnCount(4)
        self.ui.table_history.setHorizontalHeaderLabels(["Time", "Input Summary", "Predicted Price", "Model"])
        if hasattr(self.ui, "btn_export_csv"):
            self.ui.btn_export_csv.clicked.connect(self._export_csv)
        if hasattr(self.ui, "btn_export_pdf"):
            self.ui.btn_export_pdf.clicked.connect(self._export_pdf)
        try:
            self._load_persisted_history()
        except Exception:
            pass

        # Tăng tính linh hoạt cho giao diện nhỏ
        self._enhance_responsiveness()
        ok = False
        try:
            ok = self._ensure_model_for_customer()
        except Exception:
            ok = False
        if not ok:
            QMessageBox.warning(self, "Not Activate Yet", "Waiting for Admin Handling Data.")
            try:
                self.ui.tabWidget.setEnabled(False)
            except Exception:
                pass
        else:
            try:
                self.ui.tabWidget.setEnabled(True)
            except Exception:
                pass
            try:
                self.statusBar().showMessage(f"Default model: {self._get_model_default_name()}")
            except Exception:
                pass

        # Recommendation: chuẩn bị nguồn dữ liệu và kết nối sự kiện
        try:
            self._init_recommendation_ui()
        except Exception:
            pass
        if hasattr(self.ui, "btn_rec_export_csv"):
            self.ui.btn_rec_export_csv.clicked.connect(self._export_recommend_csv)
        if hasattr(self.ui, "btn_rec_export_pdf"):
            self.ui.btn_rec_export_pdf.clicked.connect(self._export_recommend_pdf)

    def _error(self, msg: str):
        QMessageBox.critical(self, "Error", msg)

    def _handle_logout(self):
        from login_app import LoginWindow
        self.close()
        self._login = LoginWindow()
        self._login.show()

    def _open_house_input_form(self):
        try:
            # no longer opens a dialog; keep method for compatibility
            if hasattr(self, "inline_house_form"):
                self.inline_house_form.show()
        except Exception:
            pass

    def _start_chatbot_server(self):
        try:
            chat_path = os.path.join(os.path.dirname(__file__), "chatbot", "chatbot.py")
            if not os.path.isfile(chat_path):
                self._error("Không tìm thấy chatbot.py")
                return
            try:
                pdf_path = os.path.join(os.path.dirname(__file__), "chatbot", "data", "house_price_knowledge.pdf")
                if not os.path.isfile(pdf_path):
                    gen_path = os.path.join(os.path.dirname(__file__), "chatbot", "data", "create_house_data_pdf.py")
                    if os.path.isfile(gen_path):
                        subprocess.run([sys.executable, gen_path], cwd=os.path.dirname(__file__), timeout=15)
            except Exception:
                pass
            target_port = 7860
            env = os.environ.copy()
            env["CHATBOT_PORT"] = str(target_port)
            env.setdefault("CHATBOT_SHARE", "false")
            env["GRADIO_SERVER_PORT"] = str(target_port)
            url = f"http://127.0.0.1:{target_port}"
            if hasattr(self.ui, "lbl_chatbot_url"):
                self.ui.lbl_chatbot_url.setText(url)
            if self._chatbot_webview is not None:
                try:
                    self._chatbot_webview.setUrl(QtCore.QUrl(url))
                except Exception:
                    pass
            try:
                self._chatbot_proc = subprocess.Popen([sys.executable, chat_path], env=env, cwd=os.path.dirname(__file__))
                try:
                    webbrowser.open(url, new=2)
                except Exception:
                    pass
            except Exception:
                try:
                    webbrowser.open(url, new=2)
                except Exception:
                    pass
        except Exception as e:
            self._error(f"Không thể khởi động chatbot: {e}")

    def _toggle_theme(self):
        try:
            self._theme_mode = "dark" if getattr(self, "_theme_mode", "light") == "light" else "light"
            self._apply_theme(self._theme_mode)
            if hasattr(self, "canvas_city_map") and hasattr(self, "ax_city_map"):
                fig_bg = "#221733" if self._theme_mode == "dark" else "#f8e1f4"
                ax_bg = "#2d2046" if self._theme_mode == "dark" else "#ffffff"
                self.canvas_city_map.figure.set_facecolor(fig_bg)
                self.ax_city_map.set_facecolor(ax_bg)
                text_color = "#FFFFFF" if self._theme_mode == "dark" else "#2b2342"
                self.ax_city_map.tick_params(colors=text_color, axis='x')
                self.ax_city_map.tick_params(colors=text_color, axis='y')
                self.ax_city_map.xaxis.label.set_color(text_color)
                self.ax_city_map.yaxis.label.set_color(text_color)
                self.ax_city_map.title.set_color(text_color)
                try:
                    if hasattr(self, "_city_cb") and self._city_cb is not None:
                        self._city_cb.set_label("Giá trung bình", color=text_color)
                        self._city_cb.ax.yaxis.set_tick_params(color=text_color)
                        for lbl in self._city_cb.ax.get_yticklabels():
                            lbl.set_color(text_color)
                except Exception:
                    pass
                self.canvas_city_map.draw_idle()
        except Exception:
            pass

    def _load_icon(self, name: str, fallback: QtWidgets.QStyle.StandardPixmap):
        icon_path = os.path.join(os.path.dirname(__file__), "UI", "icons", name)
        if os.path.isfile(icon_path):
            return QtGui.QIcon(icon_path)
        return self.style().standardIcon(fallback)

    def _mono_icon(self, kind: str, size: int = 22, color: str = "#2b2342"):
        pm = QtGui.QPixmap(size, size)
        pm.fill(QtCore.Qt.GlobalColor.transparent)
        p = QtGui.QPainter(pm)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        pen = QtGui.QPen(QtGui.QColor(color))
        pen.setWidth(2)
        p.setPen(pen)
        if kind == "predict":
            # trục và đường biểu đồ tăng
            p.drawLine(3, size - 4, size - 3, size - 4)  # trục X
            p.drawLine(3, size - 4, 3, 4)              # trục Y
            path = QtGui.QPainterPath()
            path.moveTo(4, size - 6)
            path.lineTo(size // 2 - 2, size // 2)
            path.lineTo(size - 5, 6)
            p.drawPath(path)
        elif kind == "history":
            # đồng hồ tối giản
            p.drawEllipse(4, 4, size - 8, size - 8)
            cx = size // 2
            cy = size // 2
            p.drawLine(cx, cy, cx, 7)        # kim phút
            p.drawLine(cx, cy, cx + 5, cy)   # kim giờ
        elif kind == "map":
            # ghim vị trí
            cx = size / 2
            cy = size / 2 - 2
            p.drawEllipse(int(cx - 4), int(cy - 4), 8, 8)
            poly = QtGui.QPolygon([
                QtCore.QPoint(int(cx), int(cy + 6)),
                QtCore.QPoint(int(cx - 4), size - 4),
                QtCore.QPoint(int(cx + 4), size - 4),
            ])
            p.drawPolygon(poly)
        elif kind == "recommend":
            # checklist tối giản
            p.drawRect(5, 4, size - 10, size - 8)
            p.drawLine(8, 9, size - 8, 9)
            p.drawLine(8, 13, size - 8, 13)
            p.drawLine(8, 17, size - 8, 17)
            # dấu tick
            tick = QtGui.QPainterPath()
            tick.moveTo(6, 12)
            tick.lineTo(8, 14)
            tick.lineTo(12, 10)
            p.drawPath(tick)
        elif kind == "chatbot":
            p.drawRoundedRect(4, 5, size - 8, size - 10, 4, 4)
            p.drawLine(8, size - 5, 12, size - 1)
            p.drawLine(12, size - 1, 14, size - 5)
        elif kind == "exportcsv":
            p.drawRect(4, 4, size - 8, size - 8)
            p.drawLine(6, 8, size - 6, 8)
            p.drawLine(6, 11, size - 6, 11)
            p.drawLine(6, 14, size - 6, 14)
        elif kind == "exportpdf":
            p.drawRect(4, 4, size - 8, size - 8)
            p.drawLine(6, 8, size - 10, 8)
            p.drawLine(6, 12, size - 10, 12)
        elif kind == "logout":
            p.drawRect(4, 4, size - 12, size - 8)
            p.drawLine(size - 8, 6, size - 4, 6)
            p.drawLine(size - 8, 10, size - 4, 10)
            p.drawLine(size - 4, 8, size - 1, 8)
        elif kind == "theme":
            p.drawEllipse(5, 5, size - 10, size - 10)
        elif kind == "play":
            poly = QtGui.QPolygon([QtCore.QPoint(6, 5), QtCore.QPoint(size - 6, size // 2), QtCore.QPoint(6, size - 5)])
            p.drawPolygon(poly)
        else:
            p.drawEllipse(5, 5, size - 10, size - 10)
        p.end()
        return QtGui.QIcon(pm)

    def _apply_icons(self):
        s = self.style()
        try:
            if hasattr(self.ui, "btn_toggle_theme"):
                self.ui.btn_toggle_theme.setIcon(self._mono_icon("theme"))
        except Exception:
            pass
        try:
            if hasattr(self.ui, "btn_logout"):
                self.ui.btn_logout.setIcon(self._mono_icon("logout"))
        except Exception:
            pass
        try:
            if hasattr(self.ui, "btn_export_csv"):
                self.ui.btn_export_csv.setIcon(self._mono_icon("exportcsv"))
        except Exception:
            pass
        try:
            if hasattr(self.ui, "btn_export_pdf"):
                self.ui.btn_export_pdf.setIcon(self._mono_icon("exportpdf"))
        except Exception:
            pass
        try:
            if hasattr(self.ui, "btn_rec_export_csv"):
                self.ui.btn_rec_export_csv.setIcon(self._mono_icon("exportcsv"))
        except Exception:
            pass
        try:
            if hasattr(self.ui, "btn_rec_export_pdf"):
                self.ui.btn_rec_export_pdf.setIcon(self._mono_icon("exportpdf"))
        except Exception:
            pass
        try:
            if hasattr(self.ui, "btn_start_chatbot"):
                self.ui.btn_start_chatbot.setIcon(self._mono_icon("play"))
        except Exception:
            pass
        try:
            if hasattr(self.ui, "tabWidget"):
                try:
                    self.ui.tabWidget.setIconSize(QtCore.QSize(24, 24))
                except Exception:
                    pass
                img_root = os.path.join(os.path.dirname(__file__), "images")
                def icon_from(name, kind):
                    p = os.path.join(img_root, name)
                    if os.path.isfile(p):
                        return QtGui.QIcon(p)
                    return self._mono_icon(kind)
                self.ui.tabWidget.setTabIcon(0, icon_from("PricePrediction.png", "predict"))
                self.ui.tabWidget.setTabIcon(1, icon_from("History.png", "history"))
                self.ui.tabWidget.setTabIcon(2, icon_from("Map.png", "map"))
                self.ui.tabWidget.setTabIcon(3, icon_from("Recommend.png", "recommend"))
                self.ui.tabWidget.setTabIcon(4, icon_from("Chatbot.png", "chatbot"))
        except Exception:
            pass

    def _apply_tab_titles_plain(self):
        try:
            tw = self.ui.tabWidget
            names = ["Price Prediction", "Prediction History", "Map", "Recommendation", "Chatbot"]
            for idx in range(min(tw.count(), len(names))):
                tw.setTabText(idx, names[idx])
        except Exception:
            pass

    def _normalize(self, s: str) -> str:
        import unicodedata
        s = (s or "").lower().strip()
        s = unicodedata.normalize('NFD', s)
        s = "".join(ch for ch in s if unicodedata.category(ch) != 'Mn')
        s = s.replace(" ", "").replace(".", "")
        return s

    def _coords(self):
        d = {
            "hanoi": (21.0278, 105.8342),
            "namtuliem": (21.016, 105.78),
            "haiphong": (20.844, 106.688),
            "danang": (16.054, 108.202),
            "tphcm": (10.823, 106.629),
            "vinhlong": (10.256, 105.973),
            "bentre": (10.241, 106.375),
            "haigiang": (22.833, 104.983),
            "yenbai": (21.700, 104.867),
            "tuyenquang": (21.817, 105.217),
            "sonla": (21.160, 103.767),
            "hungyen": (20.646, 106.051),
            "phutho": (21.300, 105.200),
            "binhdinh": (13.782, 109.219),
            "binhduong": (11.173, 106.673),
            "binhthuan": (10.940, 108.100),
            "lamdong": (11.946, 108.441),
            "thuathienhue": (16.463, 107.590),
            "baria vungtau": (10.411, 107.136),
            "baria": (10.411, 107.136),
            "vungtau": (10.411, 107.136),
        }
        return {self._normalize(k): v for k, v in d.items()}

    def _augment_region(self, city: str) -> str:
        city = (city or "").strip()
        if "," in city:
            return city
        key = city.lower()
        mapping = {
            "hà nội": ["Hoàn Kiếm", "Hai Bà Trưng", "Cầu Giấy", "Long Biên", "Tây Hồ", "Thanh Xuân"],
            "tp.hcm": ["Cầu Ông Lãnh", "Quận 1", "Quận 3", "Quận 7", "Thủ Đức", "Bình Thạnh"],
            "đà nẵng": ["Hải Châu", "Sơn Trà", "Ngũ Hành Sơn", "Liên Chiểu"],
            "hải phòng": ["Hồng Bàng", "Lê Chân", "Ngô Quyền"],
            "bình dương": ["Thủ Dầu Một", "Dĩ An", "Thuận An"],
            "bà rịa vũng tàu": ["Vũng Tàu", "Bà Rịa", "Long Điền"],
            "lâm đồng": ["Đà Lạt", "Bảo Lộc"],
            "thừa thiên huế": ["Huế", "Hương Thủy"],
            "hà giang": ["Trung tâm", "Quản Bạ"],
            "yên bái": ["Trung tâm", "Văn Yên"],
            "tuyên quang": ["Trung tâm", "Sơn Dương"],
        }
        def norm(s):
            return "".join(ch for ch in s.lower() if ch.isalnum())
        subs = None
        for k, v in mapping.items():
            if norm(key) == norm(k) or norm(k) in norm(key):
                subs = v
                break
        if subs is None:
            subs = ["Trung tâm", "Khu công nghiệp", "Khu dân cư", "Ven sông", "Ven biển"]
        s = np.random.choice(subs)
        return f"{s}, {city}" if city else s

    def _sample_floor(self, rng: np.random.RandomState) -> int:
        # trọng số để phần lớn nằm ở tầng 2–3
        weights = np.array([0.15, 0.4, 0.3, 0.1, 0.05])  # cho 1..5
        cum = np.cumsum(weights)
        x = float(rng.rand())
        idx = int(np.searchsorted(cum, x))
        return int(1 + idx)

    def _update_price_trend(self, current_price: float):
        try:
            if not hasattr(self, "ax_price_trend"):
                return
            try:
                self.ui.chart_view_price_trend.setVisible(True)
            except Exception:
                pass
            years = list(range(2015, 2036))
            rng = np.random.RandomState(int(current_price) % 9973)
            base_growth = 0.04
            shocks = {2020: -0.05, 2021: 0.03}
            prices = []
            p = max(1.0, float(current_price)) * 0.75
            for y in years:
                g = base_growth + rng.uniform(-0.01, 0.015) + shocks.get(y, 0.0)
                p = p * (1.0 + g)
                prices.append(p)
            ax = self.ax_price_trend
            ax.clear()
            try:
                self.canvas_price_trend.figure.set_facecolor("#ffffff")
            except Exception:
                pass
            ax.set_facecolor("#ffffff")
            ax.plot(years, prices, color="#58D68D")
            ax.set_title("Price Trend (2015–2035)", pad=8, color="#2b2342")
            ax.set_xlabel("Year", color="#2b2342")
            ax.set_ylabel("Predicted Price", color="#2b2342")
            ax.grid(True, linestyle="--", alpha=0.4)
            ax.tick_params(colors="#2b2342", axis='x')
            ax.tick_params(colors="#2b2342", axis='y')
            ax.margins(x=0.03, y=0.15)
            ax.scatter([2025], [float(current_price)], color="#2E86C1")
            try:
                self.canvas_price_trend.figure.tight_layout()
            except Exception:
                pass
            self.canvas_price_trend.draw_idle()
            try:
                self._last_predicted_price = float(current_price)
                self._last_trend_years = list(years)
                self._last_trend_prices = [float(x) for x in prices]
            except Exception:
                pass
        except Exception:
            pass

    def _update_price_breakdown(self, breakdown: dict):
        try:
            if not hasattr(self, "ax_price_breakdown") or breakdown is None:
                return
            try:
                self.ui.chart_view_price_breakdown.setVisible(True)
            except Exception:
                pass
            labels = list(breakdown.keys())
            vals = [float(breakdown[k]) for k in labels]
            s = sum(v for v in vals if v >= 0)
            if s <= 0:
                return
            min_pct = 3.0
            n = len(vals)
            base = min_pct * n
            remaining = max(0.0, 100.0 - base)
            weights = [max(0.0, v) / s for v in vals]
            sum_w = sum(weights) or 1.0
            perc = [min_pct + remaining * (w / sum_w) for w in weights]

            ax = self.ax_price_breakdown
            ax.clear()
            try:
                self.canvas_price_breakdown.figure.set_facecolor("#ffffff")
            except Exception:
                pass
            ax.set_facecolor("#ffffff")
            ax.bar(labels, perc, color=["#7FB3D5", "#76D7C4", "#F7DC6F", "#F1948A"])
            ax.set_ylabel("% of price drivers", color="#2b2342")
            ax.set_title("Price Breakdown by Features", pad=8, color="#2b2342")
            ax.grid(True, axis="y", linestyle="--", alpha=0.4)
            ax.set_ylim(0, 105)
            ax.margins(x=0.03, y=0.10)
            for i, p in enumerate(perc):
                ax.text(i, min(p + 2.0, 102.0), f"{p:,.0f}%", ha="center", va="bottom", color="#2b2342")

            try:
                self.canvas_price_breakdown.figure.tight_layout()
            except Exception:
                pass
            self.canvas_price_breakdown.draw_idle()
            try:
                self._last_breakdown = dict(zip(labels, perc))
            except Exception:
                pass
        except Exception:
            pass

    def _collect_current_inputs(self):
        d = {}
        f = getattr(self, "inline_house_form", None)
        if f is None:
            return d
        try:
            d["Area"] = f.input_area.text().strip()
            d["Frontage"] = f.input_frontage.text().strip()
            d["Floors"] = f.input_floors.text().strip()
            d["Bedrooms"] = f.input_bedrooms.text().strip()
            d["Bathrooms"] = f.input_bathrooms.text().strip()
            try:
                d["Predicted Price"] = f.lbl_result.text().strip()
            except Exception:
                pass
        except Exception:
            pass
        return d

    def _export_csv(self):
        try:
            if not hasattr(self, "_last_predicted_price"):
                self._error("No prediction yet.")
                return
            path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV (*.csv)")
            if not path:
                return
            import json
            import os
            inp = self._collect_current_inputs()
            bd = getattr(self, "_last_breakdown", {})
            top3 = sorted([(k, float(v)) for k, v in bd.items()], key=lambda x: -x[1])[:3]
            top3_str = "; ".join([f"{k}" for k, _ in top3]) if top3 else ""
            trend_years = getattr(self, "_last_trend_years", [])
            trend_prices = getattr(self, "_last_trend_prices", [])
            # Lưu hình chart ra PNG cạnh file CSV
            base, _ext = os.path.splitext(path)
            trend_png = base + "_trend.png"
            breakdown_png = base + "_breakdown.png"
            try:
                if hasattr(self, "canvas_price_trend") and self.canvas_price_trend is not None:
                    self.canvas_price_trend.figure.savefig(trend_png, dpi=150, bbox_inches='tight')
            except Exception:
                trend_png = ""
            try:
                if hasattr(self, "canvas_price_breakdown") and self.canvas_price_breakdown is not None:
                    self.canvas_price_breakdown.figure.savefig(breakdown_png, dpi=150, bbox_inches='tight')
            except Exception:
                breakdown_png = ""
            row = {
                **inp,
                "Predicted Price": float(getattr(self, "_last_predicted_price", 0.0)),
                "Top 3 strongest factors": top3_str,
                # Flatten chart values để đọc dễ trong Excel
                "Trend years": "; ".join(str(y) for y in trend_years),
                "Trend prices": "; ".join(f"{p:.4f}" for p in trend_prices),
                **{f"Breakdown - {k}": float(v) for k, v in bd.items()},
                "Trend chart file": trend_png,
                "Breakdown chart file": breakdown_png,
                # Excel (Microsoft 365) có hàm IMAGE, hiển thị ảnh trong ô
                "Trend chart": f"=IMAGE(\"file:///{trend_png.replace('\\\\', '/').replace('\\', '/')}\")" if trend_png else "",
                "Breakdown chart": f"=IMAGE(\"file:///{breakdown_png.replace('\\\\', '/').replace('\\', '/')}\")" if breakdown_png else "",
            }
            import pandas as pd
            df = pd.DataFrame([row])
            # Ghi UTF-8 with BOM để Excel hiển thị tiếng Việt đúng
            df.to_csv(path, index=False, encoding='utf-8-sig')
            try:
                self._write_xlsx_with_images(path, row, trend_png, breakdown_png)
            except Exception:
                pass
            QtWidgets.QMessageBox.information(self, "Success", f"Exported: {path}")
        except Exception as e:
            self._error(f"CSV export error: {e}")

    def _write_xlsx_with_images(self, csv_path: str, row: dict, trend_png: str, breakdown_png: str):
        from openpyxl import Workbook
        from openpyxl.drawing.image import Image as XLImage
        import os
        base, _ = os.path.splitext(csv_path)
        xlsx_path = base + ".xlsx"
        wb = Workbook()
        ws = wb.active
        ws.title = "Prediction"
        # Header and values in first rows
        headers = list(row.keys())
        values = [row[h] for h in headers]
        for c, h in enumerate(headers, start=1):
            ws.cell(row=1, column=c, value=str(h))
        for c, v in enumerate(values, start=1):
            try:
                ws.cell(row=2, column=c, value=v)
            except Exception:
                ws.cell(row=2, column=c, value=str(v))
        r_img = 4
        if trend_png and os.path.isfile(trend_png):
            try:
                img1 = XLImage(trend_png)
                ws.add_image(img1, f"A{r_img}")
                r_img += int(max(20, img1.height // 20))
            except Exception:
                pass
        if breakdown_png and os.path.isfile(breakdown_png):
            try:
                img2 = XLImage(breakdown_png)
                ws.add_image(img2, f"H4")
            except Exception:
                pass
        wb.save(xlsx_path)

    def _collect_recommend_inputs(self):
        ui = self.ui
        d = {}
        try:
            d["Budget (USD)"] = ui.input_rec_budget.text().strip()
            d["Min Area (m²)"] = ui.input_rec_min_area.text().strip()
            d["Min Bedrooms"] = ui.input_rec_min_bedrooms.text().strip()
        except Exception:
            pass
        return d

    def _collect_recommend_rows(self):
        rows = []
        tbl = self.ui.table_recommendation
        try:
            cols = [tbl.horizontalHeaderItem(i).text() for i in range(tbl.columnCount())]
        except Exception:
            cols = ["Price", "Area", "Bedrooms", "Floors", "Frontage", "City/Address"]
        for r in range(tbl.rowCount()):
            row = {}
            for c in range(tbl.columnCount()):
                try:
                    it = tbl.item(r, c)
                    row[cols[c]] = it.text() if it else ""
                except Exception:
                    row[cols[c]] = ""
            rows.append(row)
        return rows

    def _export_recommend_csv(self):
        try:
            path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV (*.csv)")
            if not path:
                return
            import csv
            base_info = self._collect_recommend_inputs()
            rows = self._collect_recommend_rows()
            if rows:
                rec_headers = list(rows[0].keys())
            else:
                rec_headers = ["Price", "Area", "Bedrooms", "Floors", "Frontage", "City/Address"]
            base_keys = ["Budget (USD)", "Min Area (m²)", "Min Bedrooms"]
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                w.writerow(["User Input"])
                w.writerow(base_keys)
                w.writerow([base_info.get(k, "") for k in base_keys])
                w.writerow([])
                w.writerow(["Recommendations"])
                w.writerow(rec_headers)
                for r in rows:
                    w.writerow([r.get(h, "") for h in rec_headers])
            try:
                self._write_recommend_xlsx(path, base_info, rows, rec_headers)
            except Exception:
                pass
            QtWidgets.QMessageBox.information(self, "Success", f"Exported: {path}")
        except Exception as e:
            self._error(f"CSV export error: {e}")

    def _write_recommend_xlsx(self, csv_path: str, base_info: dict, rows: list, headers: list):
        from openpyxl import Workbook
        from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
        import os
        base, _ = os.path.splitext(csv_path)
        xlsx_path = base + ".xlsx"
        wb = Workbook()
        ws = wb.active
        ws.title = "Recommendation"
        base_keys = ["Budget (USD)", "Min Area (m²)", "Min Bedrooms"]
        ws.cell(row=1, column=1, value="User Input")
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(base_keys))
        title_fill = PatternFill("solid", fgColor="6D1E3B")
        title_font = Font(bold=True, color="FFFFFF", size=14)
        title_align = Alignment(horizontal="center", vertical="center")
        c = ws.cell(row=1, column=1)
        c.fill = title_fill
        c.font = title_font
        c.alignment = title_align
        for col, key in enumerate(base_keys, start=1):
            ws.cell(row=2, column=col, value=key)
        for col, key in enumerate(base_keys, start=1):
            ws.cell(row=3, column=col, value=base_info.get(key, ""))
        header_fill = PatternFill("solid", fgColor="D6B6F5")
        header_font = Font(bold=True)
        header_align = Alignment(horizontal="center")
        thin = Side(style="thin", color="D6B6F5")
        border = Border(left=thin, right=thin, top=thin, bottom=thin)
        for col in range(1, len(base_keys) + 1):
            cell = ws.cell(row=2, column=col)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_align
            cell.border = border
        ws.cell(row=5, column=1, value="Recommendations")
        ws.merge_cells(start_row=5, start_column=1, end_row=5, end_column=len(headers))
        t2 = ws.cell(row=5, column=1)
        t2.fill = title_fill
        t2.font = title_font
        t2.alignment = title_align
        for col, key in enumerate(headers, start=1):
            cell = ws.cell(row=6, column=col, value=key)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_align
            cell.border = border
        start_row = 7
        for r_idx, r in enumerate(rows, start=start_row):
            for c_idx, key in enumerate(headers, start=1):
                cell = ws.cell(row=r_idx, column=c_idx, value=r.get(key, ""))
                cell.border = border
                if (r_idx - start_row) % 2 == 0:
                    cell.fill = PatternFill("solid", fgColor="F8E1F4")
        max_cols = max(len(base_keys), len(headers))
        for i in range(1, max_cols + 1):
            ws.column_dimensions[chr(64 + i)].width = 18
        wb.save(xlsx_path)

    def _export_recommend_pdf(self):
        try:
            path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF (*.pdf)")
            if not path:
                return
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_pdf import PdfPages
            import datetime
            base_info = self._collect_recommend_inputs()
            rows = self._collect_recommend_rows()
            with PdfPages(path) as pdf:
                fig1 = Figure(figsize=(8.27, 11.69))
                ax1 = fig1.add_subplot(111)
                ax1.axis('off')
                y = 0.92
                ax1.text(0.5, y, "Property Recommendations Report", ha='center', va='top', fontsize=20, fontweight='bold', color="#4c0c24")
                y -= 0.05
                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ax1.text(0.5, y, f"Generated: {ts}", ha='center', va='top', fontsize=11, color="#7b6f9e")
                y -= 0.08
                ax1.text(0.05, y, "User Input:", fontsize=13, fontweight='bold', color="#2b2342")
                for k in ["Budget (USD)", "Floor area (m²)", "Region", "Property type"]:
                    y -= 0.04
                    ax1.text(0.07, y, f"{k}: {base_info.get(k,'')}", fontsize=11, color="#2b2342")
                ax1.text(0.5, 0.84, "Recommendations", ha='center', va='top', fontsize=13, fontweight='bold', color="#4c0c24")
                if rows:
                    headers = list(rows[0].keys())
                else:
                    headers = ["Property Code", "Price", "Area", "Floor", "Match (%)", "Region", "Type"]
                data = [[r.get(h, "") for h in headers] for r in rows]
                ax2 = fig1.add_axes([0.05, 0.12, 0.90, 0.68])
                ax2.axis('off')
                ncols = len(headers)
                cw = [0.98 / ncols] * ncols
                table = ax2.table(cellText=data, colLabels=headers, loc='center', cellLoc='center', colWidths=cw)
                table.auto_set_font_size(False)
                table.set_fontsize(9)
                table.scale(1.0, 1.1)
                for c in range(len(headers)):
                    try:
                        hcell = table[0, c]
                        hcell.set_facecolor("#6d1e3b")
                        hcell.set_edgecolor("#6d1e3b")
                        hcell.get_text().set_color("#f8e1f4")
                        hcell.get_text().set_weight('bold')
                    except Exception:
                        pass
                for r in range(1, len(data) + 1):
                    for c in range(len(headers)):
                        try:
                            cell = table[r, c]
                            cell.set_edgecolor("#d6b6f5")
                            cell.set_linewidth(0.8)
                            if r % 2 == 0:
                                cell.set_facecolor("#f8e1f4")
                            else:
                                cell.set_facecolor("#ffffff")
                            cell.get_text().set_color("#2b2342")
                        except Exception:
                            pass
                pdf.savefig(fig1)
            QtWidgets.QMessageBox.information(self, "Success", f"Exported: {path}")
        except Exception as e:
            self._error(f"PDF export error: {e}")

    def _export_pdf(self):
        try:
            if not hasattr(self, "_last_predicted_price"):
                self._error("No prediction yet.")
                return
            path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF (*.pdf)")
            if not path:
                return
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_pdf import PdfPages
            import datetime
            inp = self._collect_current_inputs()
            title = "House Price Prediction Report"
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            price_val = float(getattr(self, "_last_predicted_price", 0.0))
            with PdfPages(path) as pdf:
                fig1 = Figure(figsize=(8.27, 11.69))
                ax1 = fig1.add_subplot(111)
                ax1.axis('off')
                y = 0.95
                ax1.text(0.5, y, title, ha='center', va='top', fontsize=18, fontweight='bold')
                y -= 0.05
                ax1.text(0.5, y, f"Generated: {ts}", ha='center', va='top', fontsize=10)
                y -= 0.08
                ax1.text(0.05, y, "Input Summary:", fontsize=12, fontweight='bold')
                lines = [
                    f"Floor area: {inp.get('Floor area','')}",
                    f"Bedrooms: {inp.get('Bedrooms','')}",
                    f"Bathrooms: {inp.get('Bathrooms','')}",
                    f"Property type: {inp.get('Property type','')}",
                    f"Province: {inp.get('Province','')}",
                    f"Age/Condition: {inp.get('Age/Condition','')}",
                    f"Selected amenities: {inp.get('Selected amenities','')}",
                ]
                for ln in lines:
                    y -= 0.04
                    ax1.text(0.07, y, ln, fontsize=10)
                y -= 0.06
                ax1.text(0.05, y, f"Predicted Price (USD): {price_val:,.2f}", fontsize=14, fontweight='bold')
                pdf.savefig(fig1)
                if hasattr(self, "canvas_price_trend") and self.canvas_price_trend is not None:
                    pdf.savefig(self.canvas_price_trend.figure)
                if hasattr(self, "canvas_price_breakdown") and self.canvas_price_breakdown is not None:
                    pdf.savefig(self.canvas_price_breakdown.figure)
            QtWidgets.QMessageBox.information(self, "Success", f"Exported: {path}")
        except Exception as e:
            self._error(f"PDF export error: {e}")

    def _render_city_map(self):
        if not hasattr(self, "ax_city_map"):
            return
        # Đồng bộ cách nạp dữ liệu với ml_studio_app: ưu tiên dùng self.df từ loader chung
        try:
            self._load_default_df_if_needed()
        except Exception:
            pass
        df = getattr(self, "df", None)
        if not isinstance(df, pd.DataFrame) or df.empty:
            # Không dùng đường dẫn tuyệt đối; báo lỗi rõ ràng và gợi ý thư mục data
            self._error("Không có dữ liệu để vẽ bản đồ. Vui lòng đặt CSV vào thư mục 'data' hoặc tải dữ liệu mặc định.")
            return
        ax = self.ax_city_map
        ax.clear()
        text_color = "#FFFFFF" if getattr(self, "_theme_mode", "light") == "dark" else "#2b2342"
        fig_bg = "#221733" if getattr(self, "_theme_mode", "light") == "dark" else "#f8e1f4"
        ax_bg = "#2d2046" if getattr(self, "_theme_mode", "light") == "dark" else "#ffffff"
        self.canvas_city_map.figure.set_facecolor(fig_bg)
        ax.set_facecolor(ax_bg)
        ax.tick_params(colors=text_color, axis='x')
        ax.tick_params(colors=text_color, axis='y')
        ax.xaxis.label.set_color(text_color)
        ax.yaxis.label.set_color(text_color)
        ax.title.set_color(text_color)
        if "City" not in df.columns or "Price" not in df.columns:
            ax.text(0.5, 0.5, "Thiếu cột City hoặc Price", ha="center", va="center", color=text_color)
            self.canvas_city_map.draw_idle()
            return
        grouped = df.groupby("City")["Price"].mean().reset_index()
        num_cols = df.select_dtypes(include=[float, int]).columns.tolist()
        feats = [c for c in num_cols if c.lower() != "price"]
        if feats:
            try:
                from sklearn.linear_model import LinearRegression
                m = LinearRegression()
                X = df[feats]
                y = df["Price"].astype(float)
                m.fit(X, y)
                yhat = m.predict(X)
                grouped_pred = pd.DataFrame({"City": df["City"], "Pred": yhat}).groupby("City")["Pred"].mean().reset_index()
            except Exception:
                grouped_pred = grouped.rename(columns={"Price": "Pred"})
        else:
            grouped_pred = grouped.rename(columns={"Price": "Pred"})
        merged = pd.merge(grouped, grouped_pred, on="City", how="left")
        coords = self._coords()
        xs, ys, vals, names = [], [], [], []
        actuals, preds = [], []
        for _, row in merged.iterrows():
            name = str(row["City"]).strip()
            key = self._normalize(name)
            loc = coords.get(key)
            if not loc:
                if key.startswith("thua"):
                    loc = coords.get(self._normalize("Thừa Thiên Huế"))
                elif key in ("hochiminh", "thanhphohochiminh"):
                    loc = coords.get("tphcm")
            if not loc:
                continue
            lat, lon = loc
            xs.append(lon)
            ys.append(lat)
            vals.append(float(row["Price"]))
            actuals.append(float(row["Price"]))
            preds.append(float(row.get("Pred", float(row["Price"]))))
            names.append(name)
        if not xs:
            ax.text(0.5, 0.5, "Không tìm thấy toạ độ cho các tỉnh thành", ha="center", va="center", color=text_color)
            self.canvas_city_map.draw_idle()
            return
        ax.set_xlim(102, 110)
        ax.set_ylim(8, 23)
        ax.grid(True, linestyle="--", alpha=0.3)
        try:
            from matplotlib.patches import Polygon
            coast_path = [
                (107.97, 21.50), (106.68, 20.85), (105.80, 19.80), (105.70, 18.70),
                (106.60, 17.50), (107.60, 16.47), (108.20, 16.05), (109.22, 13.78),
                (109.20, 12.25), (108.10, 10.93), (107.13, 10.41), (104.49, 10.38),
                (105.15, 9.18)
            ]
            west_border = [
                (105.10, 10.70), (105.30, 11.50), (105.70, 12.50), (105.90, 13.50),
                (106.00, 14.50), (105.80, 15.50), (105.70, 16.50), (105.50, 17.50),
                (105.40, 18.50), (105.30, 19.50), (104.00, 21.20), (103.00, 21.40),
                (103.96, 22.50), (106.75, 21.85), (107.97, 21.50)
            ]
            poly_pts = coast_path + west_border
            land_color = "#e6f2ff" if getattr(self, "_theme_mode", "light") != "dark" else "#2a2550"
            edge_color = "#93c0ff" if getattr(self, "_theme_mode", "light") != "dark" else "#cbbef5"
            ax.add_patch(Polygon(poly_pts, closed=True, facecolor=land_color, edgecolor=edge_color, linewidth=1.0, alpha=0.6))
        except Exception:
            pass
        sc = ax.scatter(xs, ys, c=vals, cmap="Blues", s=220, edgecolors='k', linewidths=0.5)
        for x, y, name in zip(xs, ys, names):
            ax.text(x + 0.1, y + 0.1, name, fontsize=9, color=text_color)
        if hasattr(self, "_city_cb") and self._city_cb is not None:
            try:
                self._city_cb.update_normal(sc)
            except Exception:
                self._city_cb = self.canvas_city_map.figure.colorbar(sc, ax=ax)
        else:
            self._city_cb = self.canvas_city_map.figure.colorbar(sc, ax=ax)
        self._city_cb.set_label("Giá trung bình", color=text_color)
        self._city_cb.ax.yaxis.set_tick_params(color=text_color)
        for lbl in self._city_cb.ax.get_yticklabels():
            lbl.set_color(text_color)
        try:
            if not hasattr(self, "_city_axpos"):
                self._city_axpos = ax.get_position()
            else:
                ax.set_position(self._city_axpos)
        except Exception:
            pass
        ax.set_xlabel("Kinh độ")
        ax.set_ylabel("Vĩ độ")
        ax.set_title("So sánh giá nhà theo các tỉnh thành trong nước")
        self._points_data = {"xs": xs, "ys": ys, "names": names, "actuals": actuals, "preds": preds}
        self.annot = ax.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points", bbox=dict(boxstyle="round", fc="#fff8dc", ec="k", alpha=0.9))
        self.annot.set_visible(False)
        self.cid_hover = self.canvas_city_map.mpl_connect("motion_notify_event", self._on_mouse_move)
        self.canvas_city_map.draw_idle()

    def _on_tab_changed(self, idx: int):
        try:
            if hasattr(self.ui, "tab_map"):
                if idx == self.ui.tabWidget.indexOf(self.ui.tab_map):
                    self._render_city_map()
        except Exception:
            pass

    def _on_mouse_move(self, event):
        if not hasattr(self, "_points_data"):
            return
        if event.inaxes != self.ax_city_map:
            self.annot.set_visible(False)
            self.canvas_city_map.draw_idle()
            return
        xs = self._points_data["xs"]
        ys = self._points_data["ys"]
        names = self._points_data["names"]
        actuals = self._points_data["actuals"]
        preds = self._points_data["preds"]
        trans = self.ax_city_map.transData.transform
        pos = np.array([event.x, event.y])
        dists = []
        for i in range(len(xs)):
            pt = trans((xs[i], ys[i]))
            dists.append(np.hypot(*(pt - pos)))
        if not dists:
            self.annot.set_visible(False)
            self.canvas_city_map.draw_idle()
            return
        i = int(np.argmin(dists))
        if dists[i] < 20:
            self.annot.xy = (xs[i], ys[i])
            txt = f"{names[i]}\nGiá thực tế: {actuals[i]:.4f}\nGiá dự đoán: {preds[i]:.4f}"
            self.annot.set_text(txt)
            fc = "#FFF59D" if getattr(self, "_theme_mode", "light") != "dark" else "#4a3976"
            ec = "#2b2342" if getattr(self, "_theme_mode", "light") != "dark" else "#FFFFFF"
            self.annot.get_bbox_patch().set_facecolor(fc)
            self.annot.get_bbox_patch().set_edgecolor(ec)
            self.annot.set_visible(True)
        else:
            self.annot.set_visible(False)
        self.canvas_city_map.draw_idle()
    # ------------ Recommendation UI & Logic ------------
    def _init_recommendation_ui(self):
        if not hasattr(self.ui, "tab_recommend"):
            return
        # gắn sự kiện chạy gợi ý
        if hasattr(self.ui, "btn_run_recommendation"):
            self.ui.btn_run_recommendation.clicked.connect(self.slot_run_recommendation)

        # chuẩn bị bảng
        if hasattr(self.ui, "table_recommendation"):
            self.ui.table_recommendation.setColumnCount(6)
            self.ui.table_recommendation.setHorizontalHeaderLabels(["Price", "Area", "Bedrooms", "Floors", "Frontage", "City/Address"])

    def _load_default_df_if_needed(self):
        if isinstance(getattr(self, "df", None), pd.DataFrame) and not self.df.empty:
            return
        try:
            import json
            data_dir = os.path.join(os.path.dirname(__file__), "data")
            meta_path = os.path.join(data_dir, "official_model_meta.json")
            candidates = []
            if os.path.isfile(meta_path):
                with open(meta_path, "r", encoding="utf-8") as mf:
                    meta = json.load(mf)
                dp = str(meta.get("dataset_path", "")).strip()
                if dp:
                    candidates.append(dp)
            candidates.append(os.path.join(data_dir, "raw_value_dataset.csv"))
            for p in candidates:
                if os.path.isfile(p):
                    self.df = pd.read_csv(p)
                    return
        except Exception:
            pass
        self.df = pd.DataFrame()

    def _find_col(self, cols, candidates):
        def norm(s):
            return "".join(ch for ch in str(s).lower() if ch.isalnum())
        m = {norm(c): c for c in cols}
        for cand in candidates:
            c = m.get(norm(cand))
            if c:
                return c
        return None

    def _vectorize(self, row, price_col, area_col, city_col, type_col, scaler):
        price = float(row.get(price_col, np.nan)) if price_col else np.nan
        area = float(row.get(area_col, np.nan)) if area_col else np.nan
        price_s, area_s = 0.0, 0.0
        try:
            v = scaler.transform([[price if not np.isnan(price) else 0.0, area if not np.isnan(area) else 0.0]])[0]
            price_s, area_s = float(v[0]), float(v[1])
        except Exception:
            price_s = (price or 0.0)
            area_s = (area or 0.0)
        region = str(row.get(city_col, "")) if city_col else ""
        ptype = str(row.get(type_col, "")) if type_col else ""
        # one-hot đơn giản: chỉ giữ đúng nhãn; phần còn lại = 0
        return price_s, area_s, region, ptype

    def slot_run_recommendation(self):
        try:
            self._load_default_df_if_needed()
            if self.df.empty:
                self._error("Không có dữ liệu bất động sản để gợi ý.")
                return
            cols = list(self.df.columns)
            price_col = self._find_col(cols, ["Price", "Giá", "Gia"]) or None
            area_col = self._find_col(cols, ["Area", "Diện tích", "Dientich"]) or None
            bedrooms_col = self._find_col(cols, ["Bedrooms", "Bed", "Phòng ngủ"]) or None
            floors_col = self._find_col(cols, ["Floors", "Floor", "Tầng", "Tang"]) or None
            frontage_col = self._find_col(cols, ["Frontage", "Mặt tiền", "Front"]) or None
            city_col = self._find_col(cols, ["City", "Region", "Location", "Province", "Address", "District"]) or None

            def _f(text):
                t = (text or "").replace("_", "").replace(",", "").strip()
                return float(t) if t else np.nan
            budget = _f(self.ui.input_rec_budget.text())
            min_area = _f(self.ui.input_rec_min_area.text())
            min_bedrooms = _f(self.ui.input_rec_min_bedrooms.text())

            if np.isnan(budget) or budget <= 0:
                self._error("Vui lòng nhập budget hợp lệ.")
                return

            df = self.df.copy()
            if price_col and not np.isnan(budget):
                try:
                    df[price_col] = pd.to_numeric(df[price_col], errors="coerce")
                    df = df[df[price_col] <= float(budget)]
                except Exception:
                    pass
            else:
                QtWidgets.QMessageBox.warning(self, "Thiếu cột", "Dữ liệu hiện tại không hỗ trợ tiêu chí ngân sách")

            if area_col and not np.isnan(min_area):
                try:
                    df[area_col] = pd.to_numeric(df[area_col], errors="coerce")
                    df = df[df[area_col] >= float(min_area)]
                except Exception:
                    pass
            elif not np.isnan(min_area):
                QtWidgets.QMessageBox.warning(self, "Thiếu cột", "Dữ liệu hiện tại không hỗ trợ tiêu chí diện tích")

            if bedrooms_col and not np.isnan(min_bedrooms):
                try:
                    df[bedrooms_col] = pd.to_numeric(df[bedrooms_col], errors="coerce")
                    df = df[df[bedrooms_col] >= float(min_bedrooms)]
                except Exception:
                    pass
            elif not np.isnan(min_bedrooms):
                QtWidgets.QMessageBox.warning(self, "Thiếu cột", "Dữ liệu hiện tại không hỗ trợ tiêu chí số phòng ngủ")

            if df.empty:
                self._error("Không có kết quả phù hợp.")
                return

            if price_col and not np.isnan(budget):
                df["_diff_budget"] = (df[price_col].astype(float) - float(budget)).abs()
                df_sorted = df.sort_values("_diff_budget", ascending=True)
            elif area_col:
                df_sorted = df.sort_values(area_col, ascending=False)
            else:
                QtWidgets.QMessageBox.warning(self, "Thiếu cột", "Dữ liệu hiện tại không hỗ trợ xếp hạng kết quả")
                df_sorted = df.copy()

            top = df_sorted.head(10)
            table = self.ui.table_recommendation
            table.clearContents()
            table.setRowCount(len(top))
            for i in range(len(top)):
                p = top.iloc[i][price_col] if price_col else np.nan
                a = top.iloc[i][area_col] if area_col else np.nan
                b = top.iloc[i][bedrooms_col] if bedrooms_col else np.nan
                f = top.iloc[i][floors_col] if floors_col else np.nan
                fr = top.iloc[i][frontage_col] if frontage_col else np.nan
                ci = top.iloc[i][city_col] if city_col else ""
                item_price = QtWidgets.QTableWidgetItem(f"{float(p):,.0f}" if not pd.isna(p) else "")
                item_price.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
                table.setItem(i, 0, item_price)
                item_area = QtWidgets.QTableWidgetItem(f"{float(a):,.2f}" if not pd.isna(a) else "")
                item_area.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
                table.setItem(i, 1, item_area)
                item_bed = QtWidgets.QTableWidgetItem(str(int(float(b))) if not pd.isna(b) else "")
                item_bed.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                table.setItem(i, 2, item_bed)
                item_floors = QtWidgets.QTableWidgetItem(str(int(float(f))) if not pd.isna(f) else "")
                item_floors.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                table.setItem(i, 3, item_floors)
                item_front = QtWidgets.QTableWidgetItem(f"{float(fr):,.2f}" if not pd.isna(fr) else "")
                item_front.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
                table.setItem(i, 4, item_front)
                item_city = QtWidgets.QTableWidgetItem(str(ci) if not pd.isna(ci) else "")
                table.setItem(i, 5, item_city)
            table.resizeColumnsToContents()
            try:
                vh = table.verticalHeader()
                vh.setDefaultSectionSize(32)
                hdr = table.horizontalHeader()
                hdr.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
            except Exception:
                pass
        except Exception as e:
            self._error(f"Recommendation error: {e}")

    def _generate_synthetic_df(self, price_col, area_col, city_col, type_col,
                                budget: float, area_req: float,
                                region_req: str, type_req: str, n: int = 400) -> pd.DataFrame:
        cols = []
        if price_col:
            cols.append(price_col)
        if area_col:
            cols.append(area_col)
        if city_col:
            cols.append(city_col)
        if type_col:
            cols.append(type_col)
        if not cols:
            return pd.DataFrame()
        rng = np.random.RandomState(9973)
        prices = np.clip(rng.normal(loc=0.92 * budget, scale=0.08 * budget, size=n), 0.5 * budget, budget)
        areas = np.clip(rng.normal(loc=area_req, scale=max(10.0, 0.25 * area_req), size=n), 20.0, 500.0)
        regions = [self._augment_region(region_req) for _ in range(n)]
        types = []
        any_token = "optional"
        for i in range(n):
            if type_req and type_req.lower() != any_token:
                if rng.rand() < 0.8:
                    types.append(type_req)
                else:
                    types.append(np.random.choice(["Apartment", "Townhouse", "Villa"]))
            else:
                types.append(np.random.choice(["Apartment", "Townhouse", "Villa"]))
        data = {}
        if price_col:
            data[price_col] = prices
        if area_col:
            data[area_col] = areas
        if city_col:
            data[city_col] = regions
        if type_col:
            data[type_col] = types
        return pd.DataFrame(data)

    def _enhance_responsiveness(self):
        from PyQt6 import QtWidgets
        self.setMinimumSize(800, 600)
        self.ui.tabWidget.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.ui.tabWidget.setUsesScrollButtons(True)

        # Bọc TẤT CẢ 5 tab bằng ScrollArea (idempotent)
        count = self.ui.tabWidget.count()
        for i in range(count):
            w = self.ui.tabWidget.widget(i)
            if not isinstance(w, QtWidgets.QScrollArea):
                title = self.ui.tabWidget.tabText(i)
                scroll = QtWidgets.QScrollArea()
                scroll.setWidgetResizable(True)
                scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
                self.ui.tabWidget.removeTab(i)
                scroll.setWidget(w)
                self.ui.tabWidget.insertTab(i, scroll, title)

        # Khu vực chart nở đều, có kích thước tối thiểu để không bị dẹp
        try:
            sp_expand = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                              QtWidgets.QSizePolicy.Policy.Expanding)
            self.ui.group_price_chart.setSizePolicy(sp_expand)
            self.ui.chart_view_price_trend.setSizePolicy(sp_expand)
            self.ui.chart_view_price_breakdown.setSizePolicy(sp_expand)
            self.ui.chart_view_price_trend.setMinimumSize(600, 320)
            self.ui.chart_view_price_breakdown.setMinimumSize(600, 320)
        except Exception:
            pass

        self._apply_responsive_flow()

    def resizeEvent(self, event: QtGui.QResizeEvent):
        super().resizeEvent(event)
        # Điều chỉnh layout chart ngang/dọc theo độ rộng cửa sổ
        self._apply_responsive_flow()

    def _apply_responsive_flow(self):
        from PyQt6 import QtWidgets
        try:
            if self.width() < 1280:
                # hẹp: xếp dọc để cuộn dọc, tránh hẹp chart
                self.ui.hbox_price_charts.setDirection(QtWidgets.QBoxLayout.Direction.TopToBottom)
            else:
                # rộng: xếp ngang
                self.ui.hbox_price_charts.setDirection(QtWidgets.QBoxLayout.Direction.LeftToRight)
        except Exception:
            pass