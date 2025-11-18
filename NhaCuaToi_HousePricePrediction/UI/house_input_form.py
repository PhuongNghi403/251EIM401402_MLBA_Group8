from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QCheckBox,
    QPushButton,
)
import pandas as pd


class HouseInputForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("House Input Form (Customer)")
        self.setModal(True)
        self._parent = parent

        self._init_mappings()
        self._build_ui()

    def _init_mappings(self):
        self.locations = [
            "District 1",
            "District 7",
            "Thu Duc",
            "Binh Thanh",
            "Tan Binh",
        ]
        self.location_income = {
            "District 1": 80000.0,
            "District 7": 65000.0,
            "Thu Duc": 55000.0,
            "Binh Thanh": 60000.0,
            "Tan Binh": 58000.0,
        }
        self.location_population = {
            "District 1": 150000.0,
            "District 7": 250000.0,
            "Thu Duc": 1000000.0,
            "Binh Thanh": 500000.0,
            "Tan Binh": 450000.0,
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

        self.input_floor_area = QLineEdit(self)
        self.lbl_err_floor_area = QLabel("", self)
        self.lbl_err_floor_area.setStyleSheet("color: #c0392b;")
        form.addRow("Floor area (m²)", self.input_floor_area)
        form.addRow("", self.lbl_err_floor_area)

        self.spin_bedrooms = QSpinBox(self)
        self.spin_bedrooms.setRange(0, 10)
        self.lbl_err_bedrooms = QLabel("", self)
        self.lbl_err_bedrooms.setStyleSheet("color: #c0392b;")
        form.addRow("Number of bedrooms", self.spin_bedrooms)
        form.addRow("", self.lbl_err_bedrooms)

        self.spin_bathrooms = QSpinBox(self)
        self.spin_bathrooms.setRange(0, 10)
        self.lbl_err_bathrooms = QLabel("", self)
        self.lbl_err_bathrooms.setStyleSheet("color: #c0392b;")
        form.addRow("Number of bathrooms", self.spin_bathrooms)
        form.addRow("", self.lbl_err_bathrooms)

        self.combo_property_type = QComboBox(self)
        self.combo_property_type.addItems(self.property_types)
        self.lbl_err_property_type = QLabel("", self)
        self.lbl_err_property_type.setStyleSheet("color: #c0392b;")
        form.addRow("Property type", self.combo_property_type)
        form.addRow("", self.lbl_err_property_type)

        self.combo_location = QComboBox(self)
        self.combo_location.addItems(self.locations)
        self.lbl_err_location = QLabel("", self)
        self.lbl_err_location.setStyleSheet("color: #c0392b;")
        form.addRow("Location (district/area)", self.combo_location)
        form.addRow("", self.lbl_err_location)

        self.combo_age = QComboBox(self)
        self.combo_age.addItems(self.age_options)
        self.lbl_err_age = QLabel("", self)
        self.lbl_err_age.setStyleSheet("color: #c0392b;")
        form.addRow("Age / condition", self.combo_age)
        form.addRow("", self.lbl_err_age)

        amenities_box = QHBoxLayout()
        self.chk_school = QCheckBox("Near school", self)
        self.chk_hospital = QCheckBox("Near hospital", self)
        self.chk_mall = QCheckBox("Near shopping mall", self)
        self.chk_park = QCheckBox("Near park", self)
        amenities_box.addWidget(self.chk_school)
        amenities_box.addWidget(self.chk_hospital)
        amenities_box.addWidget(self.chk_mall)
        amenities_box.addWidget(self.chk_park)
        form.addRow("Nearby amenities", amenities_box)

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

        self.btn_predict.clicked.connect(self._on_predict_clicked)

    def _read_and_validate(self):
        errors = {}
        floor_text = self.input_floor_area.text().strip()
        try:
            floor_area = float(floor_text)
            if floor_area <= 0:
                errors["floor_area"] = "Please enter a valid floor area greater than 0"
        except Exception:
            errors["floor_area"] = "Please enter a valid floor area greater than 0"

        bedrooms = int(self.spin_bedrooms.value())
        bathrooms = int(self.spin_bathrooms.value())
        if bedrooms < 0 or bedrooms > 10:
            errors["bedrooms"] = "Bedrooms must be between 0 and 10"
        if bathrooms < 0 or bathrooms > 10:
            errors["bathrooms"] = "Bathrooms must be between 0 and 10"

        prop_type = self.combo_property_type.currentText().strip()
        location = self.combo_location.currentText().strip()
        age_label = self.combo_age.currentText().strip()
        if not prop_type:
            errors["prop_type"] = "Please select a property type"
        if not location:
            errors["location"] = "Please select a location"
        if not age_label:
            errors["age"] = "Please select an age/condition"

        self.lbl_err_floor_area.setText(errors.get("floor_area", ""))
        self.lbl_err_bedrooms.setText(errors.get("bedrooms", ""))
        self.lbl_err_bathrooms.setText(errors.get("bathrooms", ""))
        self.lbl_err_property_type.setText(errors.get("prop_type", ""))
        self.lbl_err_location.setText(errors.get("location", ""))
        self.lbl_err_age.setText(errors.get("age", ""))

        if errors:
            return None

        amenities = {
            "NearSchool": 1 if self.chk_school.isChecked() else 0,
            "NearHospital": 1 if self.chk_hospital.isChecked() else 0,
            "NearMall": 1 if self.chk_mall.isChecked() else 0,
            "NearPark": 1 if self.chk_park.isChecked() else 0,
        }

        return {
            "FloorArea": floor_area,
            "Bedrooms": bedrooms,
            "Bathrooms": bathrooms,
            "PropertyType": prop_type,
            "Location": location,
            "AgeLabel": age_label,
            "Amenities": amenities,
        }

    def _build_feature_vector(self, clean_obj):
        req_names = list(getattr(getattr(self, "_parent", None), "model_default", None).feature_names_in_) if getattr(self._parent, "model_default", None) and hasattr(self._parent.model_default, "feature_names_in_") else []
        if not req_names:
            req_names = ["Area", "Bathrooms", "Bedrooms", "Floors", "Frontage"]

        area = float(clean_obj["FloorArea"]) if clean_obj.get("FloorArea") is not None else 0.0
        bedrooms = float(clean_obj.get("Bedrooms", 0))
        bathrooms = float(clean_obj.get("Bathrooms", 0))
        floors = max(1.0, (bedrooms + bathrooms) / 2.0)
        frontage = max(0.0, area / 10.0) + 0.5 * sum(clean_obj["Amenities"].values())

        values_by_name = {
            "Area": area,
            "Bathrooms": bathrooms,
            "Bedrooms": bedrooms,
            "Floors": float(floors),
            "Frontage": float(frontage),
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
            income = values_by_name.get("Avg Area Income", 0.0)
            age = values_by_name.get("Avg Area House Age", 0.0)
            rooms = values_by_name.get("Avg Area Number of Rooms", 0.0)
            bedrooms = values_by_name.get("Avg Area Number of Bedrooms", 0.0)
            population = values_by_name.get("Area Population", 0.0)
            pred = max(0.0, income * 100.0 + rooms * 50000.0 + bedrooms * 30000.0 + population * 0.1 - age * 10000.0)

        self.lbl_result.setText(f"Predicted Price: {pred:,.2f}")

        input_summary = {
            "AvgAreaIncome": values_by_name.get("Avg Area Income", 0.0),
            "AvgAreaHouseAge": values_by_name.get("Avg Area House Age", 0.0),
            "AvgAreaNumRooms": values_by_name.get("Avg Area Number of Rooms", 0.0),
            "AvgAreaNumBedrooms": values_by_name.get("Avg Area Number of Bedrooms", 0.0),
            "AreaPopulation": values_by_name.get("Area Population", 0.0),
        }
        try:
            self._parent.save_to_history(input_summary, pred, self._parent._get_model_default_name())
        except Exception:
            pass