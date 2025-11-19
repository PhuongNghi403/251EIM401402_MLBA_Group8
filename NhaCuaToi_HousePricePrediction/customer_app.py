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
        try:
            self._ensure_model_for_customer()
        except Exception:
            pass

        # Recommendation: chuẩn bị nguồn dữ liệu và kết nối sự kiện
        try:
            self._init_recommendation_ui()
        except Exception:
            pass

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
            target_port = 7865
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
            # nền trắng cho biểu đồ
            try:
                self.canvas_price_trend.figure.set_facecolor("#ffffff")
            except Exception:
                pass
            ax.set_facecolor("#ffffff")
            ax.plot(years, prices, color="#58D68D")
            ax.set_xlabel("Year")
            ax.set_ylabel("Predicted Price")
            ax.grid(True, linestyle="--", alpha=0.4)
            # màu chữ tối để đọc tốt trên nền trắng
            text_color = "#2b2342"
            ax.tick_params(colors=text_color, axis='x')
            ax.tick_params(colors=text_color, axis='y')
            ax.xaxis.label.set_color(text_color)
            ax.yaxis.label.set_color(text_color)
            ax.title.set_color(text_color)
            ax.scatter([2025], [float(current_price)], color="#2E86C1")
            self.canvas_price_trend.draw_idle()
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
            # phân bổ phần trăm với ngưỡng tối thiểu để không mục nào là 0%
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
            ax.set_ylabel("% of price drivers")
            ax.set_title("Price Breakdown by Features")
            ax.grid(True, axis="y", linestyle="--", alpha=0.4)
            for i, p in enumerate(perc):
                ax.text(i, p + 1.0, f"{p:,.0f}%", ha="center", va="bottom", color="#2b2342")
            self.canvas_price_breakdown.draw_idle()
        except Exception:
            pass

    def _render_city_map(self):
        if not hasattr(self, "ax_city_map"):
            return
        path = os.path.join(os.path.dirname(__file__), "data", "SuperCleaned_with_20_Random_Cities.csv")
        if not os.path.isfile(path):
            path = r"e:\251EIM401402_MLBA_Group8\NhaCuaToi_HousePricePrediction\data\SuperCleaned_with_20_Random_Cities.csv"
        try:
            df = pd.read_csv(path)
        except Exception as e:
            self._error(f"Không thể đọc dữ liệu bản đồ: {e}")
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
        # tải df nếu cần và khởi tạo danh sách region giống dropdown ở form dự đoán
        self._load_default_df_if_needed()
        regions = []
        try:
            if hasattr(self, "inline_house_form") and getattr(self.inline_house_form, "locations", None):
                regions = list(self.inline_house_form.locations)
        except Exception:
            pass
        if not regions:
            regions = [
                "Hà Nội",
                "Nam Từ Liêm",
                "Hải Phòng",
                "Đà Nẵng",
                "TP.HCM",
                "Vĩnh Long",
                "Bến Tre",
                "Hà Giang",
                "Yên Bái",
                "Tuyên Quang",
                "Sơn La",
                "Hưng Yên",
                "Phú Thọ",
                "Bình Định",
                "Bình Dương",
                "Bình Thuận",
                "Lâm Đồng",
                "Thừa Thiên Huế",
                "Bà Rịa Vũng Tàu",
            ]
        try:
            self.ui.combo_rec_region.clear()
            self.ui.combo_rec_region.addItems(regions)
            self.ui.combo_rec_region.setCurrentIndex(0)
        except Exception:
            pass
        # gắn sự kiện chạy gợi ý
        if hasattr(self.ui, "btn_run_recommendation"):
            self.ui.btn_run_recommendation.clicked.connect(self.slot_run_recommendation)

        # chuẩn bị bảng
        if hasattr(self.ui, "table_recommendation"):
            self.ui.table_recommendation.setColumnCount(7)
            self.ui.table_recommendation.setHorizontalHeaderLabels(["Property Code", "Price", "Area", "Floor", "Match (%)", "Region", "Type"])

    def _load_default_df_if_needed(self):
        if isinstance(getattr(self, "df", None), pd.DataFrame) and not self.df.empty:
            return
        try:
            csv_candidates = [
                os.path.join(os.path.dirname(__file__), "data", "USA_Housing.csv"),
                os.path.join(os.path.dirname(__file__), "data", "SuperCleaned_vietnam_housing_dataset.csv"),
            ]
            for p in csv_candidates:
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
            # Xác định các cột
            cols = list(self.df.columns)
            price_col = self._find_col(cols, ["Price", "price", "Giá", "Gia"]) or None
            area_col = self._find_col(cols, ["Area", "Diện tích", "Dientich"]) or None
            city_col = self._find_col(cols, ["City", "Region", "Location", "Province"]) or None
            type_col = self._find_col(cols, ["Type", "PropertyType", "Loainha"]) or None
            floor_col = self._find_col(cols, ["Floors", "Floor", "Tang", "Tầng"]) or None

            # Đọc input
            def _f(text):
                t = (text or "").replace("_", "").replace(",", "").strip()
                return float(t) if t else np.nan
            budget = _f(self.ui.input_rec_budget.text())
            area_req = _f(self.ui.input_rec_area.text())
            region_req = self.ui.combo_rec_region.currentText().strip()
            type_req = self.ui.combo_rec_type.currentText().strip()
            # Kiểm tra
            if np.isnan(budget) or budget <= 0:
                self._error("Vui lòng nhập budget hợp lệ.")
                return
            if np.isnan(area_req) or area_req <= 0:
                self._error("Vui lòng nhập diện tích hợp lệ.")
                return

            # Lọc sơ bộ: giá phải <= budget
            df = self.df.copy()
            if price_col:
                df[price_col] = df[price_col].astype(float)
                df = df[df[price_col] <= float(budget)]
            if city_col and region_req:
                df = df[df[city_col].astype(str).str.lower().str.contains(region_req.lower())]
            any_token = "optional"
            if type_col and type_req and type_req.lower() != any_token:
                df = df[df[type_col].astype(str).str.lower() == type_req.lower()]
            if df.empty:
                df = self.df.copy()
                # nếu dữ liệu thật không phù hợp theo đơn vị giá, bổ sung dữ liệu giả lập
            # Chèn dữ liệu giả lập để đảm bảo có nhiều kết quả và đúng đơn vị giá
            try:
                df_synth = self._generate_synthetic_df(
                    price_col, area_col, city_col, type_col,
                    budget, area_req, region_req, type_req, n=400
                )
                df = pd.concat([df, df_synth], axis=0, ignore_index=True)
            except Exception:
                pass

            # Chuẩn hóa giá/diện tích
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            try:
                px = df[price_col].astype(float) if price_col else pd.Series([0.0] * len(df))
                ar = df[area_col].astype(float) if area_col else pd.Series([0.0] * len(df))
                scaler.fit(np.c_[px.fillna(0.0).values, ar.fillna(0.0).values])
            except Exception:
                scaler = StandardScaler(with_mean=False, with_std=False)

            # Vector người dùng
            try:
                user_vec = scaler.transform([[budget, area_req]])[0]
            except Exception:
                user_vec = np.array([budget, area_req], dtype=float)

            # Tính điểm cho từng property
            results = []
            for idx, row in df.iterrows():
                price_s, area_s, region, ptype = self._vectorize(row, price_col, area_col, city_col, type_col, scaler)
                prop_vec = np.array([price_s, area_s], dtype=float)
                # Cosine similarity
                num = float(np.dot(user_vec, prop_vec))
                den = float(np.linalg.norm(user_vec) * np.linalg.norm(prop_vec))
                cos = (num / den) if den > 1e-9 else 0.0
                # Euclidean trên vector đã scale
                dist = float(np.linalg.norm(user_vec - prop_vec))
                # Floor
                try:
                    if floor_col:
                        floor_val = int(float(row.get(floor_col, np.nan)))
                        if floor_val <= 0:
                            raise ValueError()
                    else:
                        rng = np.random.RandomState(int(idx) % 9973)
                        floor_val = self._sample_floor(rng)
                except Exception:
                    rng = np.random.RandomState((int(idx) * 17) % 9973)
                    floor_val = self._sample_floor(rng)
                # Điểm tổng hợp: 0.7*cos - 0.3*norm_dist (đưa dist về [0,1])
                results.append({
                    "ID": int(idx),
                    "Title": f"Property #{int(idx)}",
                    "Price": float(row.get(price_col, np.nan)) if price_col else np.nan,
                    "Area": float(row.get(area_col, np.nan)) if area_col else np.nan,
                    "Floor": floor_val,
                    "Region": self._augment_region(region if region else region_req),
                    "Type": (np.random.choice(["Apartment", "Townhouse", "Villa"]) if type_req.lower() == any_token else (ptype or type_req)),
                    "Cos": cos,
                    "Dist": dist,
                })

            if not results:
                self._error("Không có kết quả phù hợp.")
                return
            # Chuẩn hóa dist để tính điểm
            dists = np.array([r["Dist"] for r in results], dtype=float)
            dmin, dmax = float(dists.min()), float(dists.max())
            for r in results:
                nd = 0.0 if dmax <= dmin else (r["Dist"] - dmin) / (dmax - dmin)
                r["Score"] = 0.7 * r["Cos"] - 0.3 * nd

            # Xếp hạng
            results = [r for r in results if (not np.isnan(r.get("Price", np.nan))) and (r["Price"] <= float(budget))]
            results.sort(key=lambda r: (-r["Score"], r["Dist"]))
            top5 = results[:5]

            # Hiển thị bảng
            table = self.ui.table_recommendation
            table.clearContents()
            table.setRowCount(len(top5))
            for i, r in enumerate(top5):
                code = f"P{int(r['ID']):05d}"
                item_code = QtWidgets.QTableWidgetItem(code)
                item_code.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                table.setItem(i, 0, item_code)

                item_price = QtWidgets.QTableWidgetItem(f"{r['Price']:,.0f}" if not np.isnan(r['Price']) else "")
                item_price.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
                table.setItem(i, 1, item_price)

                item_area = QtWidgets.QTableWidgetItem(f"{r['Area']:,.2f}" if not np.isnan(r['Area']) else "")
                item_area.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
                table.setItem(i, 2, item_area)

                item_floor = QtWidgets.QTableWidgetItem(str(int(r.get("Floor", 1))))
                item_floor.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                table.setItem(i, 3, item_floor)

                cos = r.get("Cos", None)
                cos_str = f"{float(cos)*100:.2f}%" if (cos is not None and np.isfinite(cos)) else ""
                item_cos = QtWidgets.QTableWidgetItem(cos_str)
                item_cos.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                table.setItem(i, 4, item_cos)

                item_region = QtWidgets.QTableWidgetItem(str(r["Region"]))
                table.setItem(i, 5, item_region)

                item_type = QtWidgets.QTableWidgetItem(str(r["Type"]))
                table.setItem(i, 6, item_type)
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