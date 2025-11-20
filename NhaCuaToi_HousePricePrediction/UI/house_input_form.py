from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
import pandas as pd


class HouseInputForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("House Input Form (Customer)")
        self.setModal(True)
        self._parent = parent

        self._build_ui()

    def _init_mappings(self):
        self.locations = [
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
        self.location_income = {
            "Hà Nội": 90000.0,
            "Nam Từ Liêm": 80000.0,
            "Hải Phòng": 70000.0,
            "Đà Nẵng": 75000.0,
            "TP.HCM": 95000.0,
            "Vĩnh Long": 55000.0,
            "Bến Tre": 52000.0,
            "Hà Giang": 42000.0,
            "Yên Bái": 45000.0,
            "Tuyên Quang": 46000.0,
            "Sơn La": 44000.0,
            "Hưng Yên": 60000.0,
            "Phú Thọ": 50000.0,
            "Bình Định": 52000.0,
            "Bình Dương": 70000.0,
            "Bình Thuận": 53000.0,
            "Lâm Đồng": 58000.0,
            "Thừa Thiên Huế": 56000.0,
            "Bà Rịa Vũng Tàu": 68000.0,
        }
        self.location_population = {
            "Hà Nội": 8000000.0,
            "Nam Từ Liêm": 1000000.0,
            "Hải Phòng": 2000000.0,
            "Đà Nẵng": 1100000.0,
            "TP.HCM": 9000000.0,
            "Vĩnh Long": 1000000.0,
            "Bến Tre": 1200000.0,
            "Hà Giang": 800000.0,
            "Yên Bái": 800000.0,
            "Tuyên Quang": 700000.0,
            "Sơn La": 1200000.0,
            "Hưng Yên": 1200000.0,
            "Phú Thọ": 1400000.0,
            "Bình Định": 1500000.0,
            "Bình Dương": 2500000.0,
            "Bình Thuận": 1200000.0,
            "Lâm Đồng": 1300000.0,
            "Thừa Thiên Huế": 1100000.0,
            "Bà Rịa Vũng Tàu": 1200000.0,
        }
        self.property_types = ["Apartment", "Townhouse", "Villa"]
        self.age_options = ["New", "< 5 years", "5–10 years", "> 10 years"]
        self.age_to_value = {
            "New": 0.0,
            "< 5 years": 4.0,
            "5–10 years": 8.0,
            "> 10 years": 12.0,
        }

    def _build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

        sp_fix = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)

        self.input_area = QLineEdit(self)
        self.input_area.setSizePolicy(sp_fix)
        self.input_area.setMinimumWidth(360)
        self.input_area.setMaximumWidth(360)
        self.input_area.setMinimumHeight(30)
        self.lbl_err_area = QLabel("", self)
        form.addRow("Area (m²)", self.input_area)
        form.addRow("", self.lbl_err_area)

        self.input_frontage = QLineEdit(self)
        self.input_frontage.setSizePolicy(sp_fix)
        self.input_frontage.setMinimumWidth(360)
        self.input_frontage.setMaximumWidth(360)
        self.input_frontage.setMinimumHeight(30)
        self.lbl_err_frontage = QLabel("", self)
        form.addRow("Frontage (m)", self.input_frontage)
        form.addRow("", self.lbl_err_frontage)

        self.input_floors = QLineEdit(self)
        self.input_floors.setSizePolicy(sp_fix)
        self.input_floors.setMinimumWidth(360)
        self.input_floors.setMaximumWidth(360)
        self.input_floors.setMinimumHeight(30)
        self.lbl_err_floors = QLabel("", self)
        form.addRow("Floors", self.input_floors)
        form.addRow("", self.lbl_err_floors)

        self.input_bedrooms = QLineEdit(self)
        self.input_bedrooms.setSizePolicy(sp_fix)
        self.input_bedrooms.setMinimumWidth(360)
        self.input_bedrooms.setMaximumWidth(360)
        self.input_bedrooms.setMinimumHeight(30)
        self.lbl_err_bedrooms = QLabel("", self)
        form.addRow("Bedrooms", self.input_bedrooms)
        form.addRow("", self.lbl_err_bedrooms)

        self.input_bathrooms = QLineEdit(self)
        self.input_bathrooms.setSizePolicy(sp_fix)
        self.input_bathrooms.setMinimumWidth(360)
        self.input_bathrooms.setMaximumWidth(360)
        self.input_bathrooms.setMinimumHeight(30)
        self.lbl_err_bathrooms = QLabel("", self)
        form.addRow("Bathrooms", self.input_bathrooms)
        form.addRow("", self.lbl_err_bathrooms)

        layout.addLayout(form)

        self.btn_predict = QPushButton("Predict Price", self)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.btn_predict.setFont(font)
        layout.addWidget(self.btn_predict)

        self.lbl_result = QLabel("", self)
        font2 = QtGui.QFont()
        font2.setPointSize(18)
        font2.setBold(True)
        self.lbl_result.setFont(font2)
        self.lbl_result.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_result)

        self.lbl_price_range = QLabel("", self)
        font_small = QtGui.QFont()
        font_small.setPointSize(12)
        font_small.setItalic(True)
        self.lbl_price_range.setFont(font_small)
        self.lbl_price_range.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        try:
            color = "#cbbef5" if getattr(self._parent, "_theme_mode", "light") == "dark" else "#7b6f9e"
        except Exception:
            color = "#7b6f9e"
        self.lbl_price_range.setStyleSheet(f"color: {color};")
        layout.addWidget(self.lbl_price_range)

        self.btn_predict.clicked.connect(self._on_predict_clicked)

    def _read_and_validate(self):
        errors = {}
        def parse(line_edit):
            t = line_edit.text().strip()
            try:
                return float(t)
            except Exception:
                return None
        area = parse(self.input_area)
        frontage = parse(self.input_frontage)
        floors = parse(self.input_floors)
        bedrooms = parse(self.input_bedrooms)
        bathrooms = parse(self.input_bathrooms)
        if area is None or area <= 0:
            errors["area"] = "Please enter a valid area"
        if frontage is None or frontage < 0:
            errors["frontage"] = "Please enter a valid frontage"
        if floors is None or floors <= 0:
            errors["floors"] = "Please enter valid floors"
        if bedrooms is None or bedrooms < 0:
            errors["bedrooms"] = "Please enter valid bedrooms"
        if bathrooms is None or bathrooms < 0:
            errors["bathrooms"] = "Please enter valid bathrooms"
        self.lbl_err_area.setText(errors.get("area", ""))
        self.lbl_err_frontage.setText(errors.get("frontage", ""))
        self.lbl_err_floors.setText(errors.get("floors", ""))
        self.lbl_err_bedrooms.setText(errors.get("bedrooms", ""))
        self.lbl_err_bathrooms.setText(errors.get("bathrooms", ""))
        if errors:
            return None
        return {
            "Area": area,
            "Frontage": frontage,
            "Floors": floors,
            "Bedrooms": bedrooms,
            "Bathrooms": bathrooms,
        }

    def _build_feature_vector(self, clean_obj):
        req_names = []
        try:
            if getattr(self._parent, "model_default", None) and hasattr(self._parent.model_default, "feature_names_in_"):
                req_names = list(getattr(self._parent.model_default, "feature_names_in_", []))
        except Exception:
            req_names = []
        if not req_names or len(req_names) != 5:
            req_names = ["Area", "Frontage", "Floors", "Bedrooms", "Bathrooms"]
        values_by_name = {
            "Area": float(clean_obj.get("Area", 0.0) or 0.0),
            "Frontage": float(clean_obj.get("Frontage", 0.0) or 0.0),
            "Floors": float(clean_obj.get("Floors", 0.0) or 0.0),
            "Bedrooms": float(clean_obj.get("Bedrooms", 0.0) or 0.0),
            "Bathrooms": float(clean_obj.get("Bathrooms", 0.0) or 0.0),
        }
        cols = []
        vals = []
        for name in req_names:
            cols.append(name)
            vals.append(float(values_by_name.get(name, 0.0)))
        return pd.DataFrame([vals], columns=cols), values_by_name

    def _on_predict_clicked(self):
        if not getattr(self._parent, "model_default", None):
            try:
                self._parent._ensure_model_for_customer()
            except Exception:
                pass

        clean = self._read_and_validate()
        if clean is None:
            return

        X_df, values_by_name = self._build_feature_vector(clean)
        pred = None
        if getattr(self._parent, "model_default", None):
            try:
                pred = float(self._parent.model_default.predict(X_df)[0])
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Prediction failed: {e}")
                return
        else:
            pred = 0.0
        self.lbl_result.setText(f"Predicted Price (Million USD): {pred:,.2f}")
        try:
            var = 0.10
            low = max(0.0, pred * (1.0 - var))
            high = pred * (1.0 + var)
            color = "#cbbef5" if getattr(self._parent, "_theme_mode", "light") == "dark" else "#7b6f9e"
            self.lbl_price_range.setStyleSheet(f"color: {color};")
            self.lbl_price_range.setText(f"Price Range (Million USD): {low:,.2f} – {high:,.2f}")
        except Exception:
            self.lbl_price_range.setText("")
        try:
            if hasattr(self._parent, "_update_price_trend"):
                self._parent._update_price_trend(pred)
        except Exception:
            pass
        try:
            breakdown = self._compute_breakdown(values_by_name)
            if hasattr(self._parent, "_update_price_breakdown"):
                self._parent._update_price_breakdown(breakdown)
        except Exception:
            pass
        input_summary = values_by_name
        try:
            self._parent.save_to_history(input_summary, pred, self._parent._get_model_default_name())
        except Exception:
            pass

    def _compute_breakdown(self, values):
        labels = ["Area", "Frontage", "Floors", "Bedrooms", "Bathrooms"]
        vals = [float(values.get(k, 0.0)) for k in labels]
        s = sum(v for v in vals if v >= 0)
        if s <= 0:
            return {k: 20.0 for k in labels}
        min_pct = 3.0
        n = len(vals)
        base = min_pct * n
        remaining = max(0.0, 100.0 - base)
        weights = [max(0.0, v) / s for v in vals]
        sum_w = sum(weights) or 1.0
        perc = [min_pct + remaining * (w / sum_w) for w in weights]
        return {labels[i]: perc[i] for i in range(n)}