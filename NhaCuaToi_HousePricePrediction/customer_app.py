from PyQt6 import QtWidgets, QtGui, QtCore
import sys
import subprocess
import pandas as pd
import numpy as np
from PyQt6.QtWidgets import QMainWindow, QMessageBox
import os
import importlib.util
import webbrowser
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
        try:
            self._vn_shapes = None
        except Exception:
            self._vn_shapes = None

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
            if hasattr(self.ui, "lbl_chatbot_url"):
                self.ui.lbl_chatbot_url.setText("URL: đang khởi động...")
            ports = [7860, 7861, 7862]
            started = False
            for p in ports:
                env = os.environ.copy()
                env["CHATBOT_PORT"] = str(p)
                env.setdefault("CHATBOT_SHARE", "false")
                try:
                    self._chatbot_proc = subprocess.Popen([sys.executable, chat_path], env=env, cwd=os.path.dirname(__file__))
                    url = f"http://127.0.0.1:{p}"
                    if hasattr(self.ui, "lbl_chatbot_url"):
                        self.ui.lbl_chatbot_url.setText(f"URL: {url}")
                    if self._chatbot_webview is not None:
                        self._chatbot_webview.setUrl(QtCore.QUrl(url))
                    else:
                        try:
                            webbrowser.open(url)
                        except Exception:
                            pass
                    started = True
                    break
                except Exception:
                    continue
            if not started:
                self._error("Không thể khởi động server Chatbot")
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
        ax.set_xlim(102, 116)
        ax.set_ylim(8, 23)
        ax.grid(True, linestyle="--", alpha=0.3)
        try:
            from matplotlib.patches import Polygon
            land_color = "#e6f2ff" if getattr(self, "_theme_mode", "light") != "dark" else "#2a2550"
            edge_color = "#93c0ff" if getattr(self, "_theme_mode", "light") != "dark" else "#cbbef5"
            shapes = self._vn_shapes or self._load_vietnam_shapes()
            if shapes and shapes.get("mainland"):
                ax.add_patch(Polygon(shapes["mainland"], closed=True, facecolor=land_color, edgecolor=edge_color, linewidth=1.0, alpha=0.6))
            else:
                fallback = [
                    (109.5, 21.5), (108.9, 20.8), (108.0, 19.5), (107.2, 18.3),
                    (106.5, 17.1), (107.8, 16.1), (108.6, 15.0), (109.2, 13.8),
                    (109.1, 12.7), (108.6, 11.4), (107.9, 10.8), (107.0, 10.5),
                    (106.3, 10.1), (105.5, 9.8), (104.9, 10.1), (104.6, 10.6),
                    (104.8, 11.4), (105.0, 12.2), (105.2, 13.2), (105.6, 14.8),
                    (105.6, 16.0), (105.1, 17.5), (104.7, 19.0), (104.2, 20.3),
                    (105.3, 21.4), (106.6, 21.7), (108.0, 21.9), (109.0, 21.7)
                ]
                ax.add_patch(Polygon(fallback, closed=True, facecolor=land_color, edgecolor=edge_color, linewidth=1.0, alpha=0.6))
            for poly in shapes.get("paracel", []):
                ax.add_patch(Polygon(poly, closed=True, facecolor=land_color, edgecolor=edge_color, linewidth=0.8, alpha=0.7))
            for poly in shapes.get("spratly", []):
                ax.add_patch(Polygon(poly, closed=True, facecolor=land_color, edgecolor=edge_color, linewidth=0.8, alpha=0.7))
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

    def _load_vietnam_shapes(self):
        try:
            base = os.path.dirname(__file__)
            docx_path = os.path.join(base, "vietnam.docx")
            if not os.path.isfile(docx_path):
                docx_path = os.path.join(os.path.dirname(base), "NhaCuaToi_HousePricePrediction", "vietnam.docx")
            import zipfile, re
            if not os.path.isfile(docx_path):
                self._vn_shapes = {"mainland": None, "paracel": [], "spratly": []}
                return self._vn_shapes
            with zipfile.ZipFile(docx_path) as z:
                data = z.read("word/document.xml").decode("utf-8", errors="ignore")
            texts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", data, flags=re.S)
            plain = " ".join(t.strip() for t in texts if t.strip())
            norm = self._normalize(plain)
            nums = re.findall(r"-?\d+(?:\.\d+)?", plain)
            vals = [float(x) for x in nums]
            pairs = []
            i = 0
            while i + 1 < len(vals):
                a = vals[i]
                b = vals[i + 1]
                if 7.0 <= min(a, b) <= 25.0 and 100.0 <= max(a, b) <= 120.0:
                    if a < b:
                        lat = a
                        lon = b
                    else:
                        lat = b
                        lon = a
                    pairs.append((lon, lat))
                i += 2
            mainland = [p for p in pairs if 102.0 <= p[0] <= 110.5 and 8.0 <= p[1] <= 23.5]
            paracel = [p for p in pairs if 111.0 <= p[0] <= 114.5 and 15.0 <= p[1] <= 17.5]
            spratly = [p for p in pairs if 111.0 <= p[0] <= 117.5 and 7.5 <= p[1] <= 13.5]
            def chain_to_polys(seq, gap=0.8):
                polys = []
                cur = []
                prev = None
                for p in seq:
                    if prev is None:
                        cur.append(p)
                    else:
                        d = abs(p[0] - prev[0]) + abs(p[1] - prev[1])
                        if d > gap and len(cur) >= 3:
                            polys.append(cur)
                            cur = [p]
                        else:
                            cur.append(p)
                    prev = p
                if len(cur) >= 3:
                    polys.append(cur)
                return polys
            mainland_poly = mainland if len(mainland) >= 3 else None
            paracel_polys = chain_to_polys(paracel)
            spratly_polys = chain_to_polys(spratly)
            self._vn_shapes = {"mainland": mainland_poly, "paracel": paracel_polys, "spratly": spratly_polys}
            return self._vn_shapes
        except Exception:
            self._vn_shapes = {"mainland": None, "paracel": [], "spratly": []}
            return self._vn_shapes