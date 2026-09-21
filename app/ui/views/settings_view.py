from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from app import __version__
from app.services.settings_service import get_settings, update_business_name
from app.services.auth_service import AuthService
from app.database.connection import get_db_path


class SettingsView(QWidget):
    settings_changed = Signal()

    def __init__(self, db_path: str = None, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.auth_service = AuthService(self.db_path)

        self.init_ui()
        self.load_data()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Title
        title = QLabel("Settings")
        title.setProperty("class", "page-title")
        layout.addWidget(title)

        # Card 1: Business Name
        card1 = QFrame()
        card1.setProperty("class", "card")
        l1 = QVBoxLayout(card1)
        l1.setSpacing(12)

        t1 = QLabel("BUSINESS NAME")
        t1.setProperty("class", "card-title")
        l1.addWidget(t1)

        l1.addWidget(QLabel("Business Name"))
        self.biz_name_input = QLineEdit()
        self.biz_name_input.setPlaceholderText("e.g. Chirathma Flora")
        l1.addWidget(self.biz_name_input)

        b1_layout = QHBoxLayout()
        b1_layout.addStretch()
        self.save_name_btn = QPushButton("Save Business Name")
        self.save_name_btn.setProperty("class", "primary-btn")
        self.save_name_btn.setCursor(Qt.PointingHandCursor)
        self.save_name_btn.clicked.connect(self.on_save_business_name)
        b1_layout.addWidget(self.save_name_btn)
        l1.addLayout(b1_layout)

        layout.addWidget(card1)

        # Card 2: Change PIN
        card2 = QFrame()
        card2.setProperty("class", "card")
        l2 = QVBoxLayout(card2)
        l2.setSpacing(12)

        t2 = QLabel("CHANGE SECURITY PIN")
        t2.setProperty("class", "card-title")
        l2.addWidget(t2)

        l2.addWidget(QLabel("Current PIN"))
        self.curr_pin_input = QLineEdit()
        self.curr_pin_input.setEchoMode(QLineEdit.Password)
        self.curr_pin_input.setMaxLength(4)
        self.curr_pin_input.setPlaceholderText("• • • •")
        l2.addWidget(self.curr_pin_input)

        l2.addWidget(QLabel("New 4-Digit PIN"))
        self.new_pin_input = QLineEdit()
        self.new_pin_input.setEchoMode(QLineEdit.Password)
        self.new_pin_input.setMaxLength(4)
        self.new_pin_input.setPlaceholderText("• • • •")
        l2.addWidget(self.new_pin_input)

        l2.addWidget(QLabel("Confirm New PIN"))
        self.confirm_pin_input = QLineEdit()
        self.confirm_pin_input.setEchoMode(QLineEdit.Password)
        self.confirm_pin_input.setMaxLength(4)
        self.confirm_pin_input.setPlaceholderText("• • • •")
        l2.addWidget(self.confirm_pin_input)

        b2_layout = QHBoxLayout()
        b2_layout.addStretch()
        self.change_pin_btn = QPushButton("Change PIN")
        self.change_pin_btn.setProperty("class", "primary-btn")
        self.change_pin_btn.setCursor(Qt.PointingHandCursor)
        self.change_pin_btn.clicked.connect(self.on_change_pin)
        b2_layout.addWidget(self.change_pin_btn)
        l2.addLayout(b2_layout)

        layout.addWidget(card2)

        # Card 3: Application & Data Info
        card3 = QFrame()
        card3.setProperty("class", "card")
        l3 = QVBoxLayout(card3)
        l3.setSpacing(8)

        t3 = QLabel("APPLICATION INFORMATION")
        t3.setProperty("class", "card-title")
        l3.addWidget(t3)

        v_lbl = QLabel(f"Application Version: {__version__}")
        v_lbl.setStyleSheet("color: #475569;")
        l3.addWidget(v_lbl)

        db_lbl = QLabel(f"Database Location: {get_db_path(self.db_path)}")
        db_lbl.setStyleSheet("color: #475569;")
        db_lbl.setWordWrap(True)
        l3.addWidget(db_lbl)

        layout.addWidget(card3)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def load_data(self):
        settings = get_settings(self.db_path)
        self.biz_name_input.setText(settings.business_name)

    def on_save_business_name(self):
        new_name = self.biz_name_input.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Validation Error", "Business name cannot be empty.")
            return

        try:
            update_business_name(new_name, self.db_path)
            QMessageBox.information(self, "Settings Saved", "Business name updated successfully.")
            self.settings_changed.emit()
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Could not update business name: {str(ex)}")

    def on_change_pin(self):
        curr_pin = self.curr_pin_input.text().strip()
        new_pin = self.new_pin_input.text().strip()
        confirm_pin = self.confirm_pin_input.text().strip()

        try:
            self.auth_service.change_pin(curr_pin, new_pin, confirm_pin)
            QMessageBox.information(self, "PIN Changed", "Your 4-digit PIN has been changed successfully.")
            self.curr_pin_input.clear()
            self.new_pin_input.clear()
            self.confirm_pin_input.clear()
        except ValueError as ve:
            QMessageBox.warning(self, "Validation Error", str(ve))
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Could not change PIN: {str(ex)}")
