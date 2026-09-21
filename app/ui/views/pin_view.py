from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QFrame
)
from PySide6.QtCore import Qt, Signal
from app.services.auth_service import AuthService
from app.services.settings_service import get_settings


class PinDialog(QDialog):
    unlocked = Signal()

    def __init__(self, auth_service: AuthService, parent=None):
        super().__init__(parent)
        self.auth_service = auth_service
        self.is_setup_mode = self.auth_service.is_first_launch()

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setFixedSize(400, 480)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 40, 30, 40)
        main_layout.setSpacing(20)

        # Card Container
        card = QFrame()
        card.setProperty("class", "card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(16)
        card_layout.setAlignment(Qt.AlignCenter)

        # Business Title
        settings = get_settings(self.auth_service.db_path)
        self.title_label = QLabel(settings.business_name)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #0284C7;")
        card_layout.addWidget(self.title_label)

        # Mode Header
        header_text = "Create 4-Digit PIN" if self.is_setup_mode else "Enter PIN"
        self.header_label = QLabel(header_text)
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #334155;")
        card_layout.addWidget(self.header_label)

        subtext = (
            "Set a 4-digit security PIN for your accounts."
            if self.is_setup_mode
            else "Enter your 4-digit PIN to access the application."
        )
        self.sub_label = QLabel(subtext)
        self.sub_label.setAlignment(Qt.AlignCenter)
        self.sub_label.setWordWrap(True)
        self.sub_label.setProperty("class", "subtext")
        card_layout.addWidget(self.sub_label)

        card_layout.addSpacing(10)

        # PIN Input Field 1
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setMaxLength(4)
        self.pin_input.setAlignment(Qt.AlignCenter)
        self.pin_input.setPlaceholderText("• • • •")
        self.pin_input.setStyleSheet("font-size: 22px; letter-spacing: 8px; font-weight: bold; padding: 10px;")
        card_layout.addWidget(self.pin_input)

        # Confirm PIN Input Field (Setup mode only)
        if self.is_setup_mode:
            self.confirm_pin_input = QLineEdit()
            self.confirm_pin_input.setEchoMode(QLineEdit.Password)
            self.confirm_pin_input.setMaxLength(4)
            self.confirm_pin_input.setAlignment(Qt.AlignCenter)
            self.confirm_pin_input.setPlaceholderText("Confirm • • • •")
            self.confirm_pin_input.setStyleSheet("font-size: 22px; letter-spacing: 8px; font-weight: bold; padding: 10px;")
            card_layout.addWidget(self.confirm_pin_input)

        card_layout.addSpacing(10)

        # Submit Button
        btn_text = "Save & Unlock" if self.is_setup_mode else "Unlock"
        self.submit_btn = QPushButton(btn_text)
        self.submit_btn.setProperty("class", "primary-btn")
        self.submit_btn.setFixedHeight(44)
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        self.submit_btn.clicked.connect(self.on_submit)
        card_layout.addWidget(self.submit_btn)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("color: #E11D48; font-size: 13px; font-weight: 500;")
        card_layout.addWidget(self.error_label)

        main_layout.addWidget(card)
        self.setLayout(main_layout)

        # Focus pin input
        self.pin_input.setFocus()
        self.pin_input.returnPressed.connect(self.on_submit)
        if self.is_setup_mode:
            self.confirm_pin_input.returnPressed.connect(self.on_submit)

    def on_submit(self):
        self.error_label.setText("")
        pin = self.pin_input.text().strip()

        if self.is_setup_mode:
            confirm_pin = self.confirm_pin_input.text().strip()
            try:
                self.auth_service.setup_pin(pin, confirm_pin)
                self.accept()
            except ValueError as e:
                self.error_label.setText(str(e))
                self.pin_input.clear()
                self.confirm_pin_input.clear()
                self.pin_input.setFocus()
        else:
            if self.auth_service.verify(pin):
                self.accept()
            else:
                self.error_label.setText("Incorrect PIN. Please try again.")
                self.pin_input.clear()
                self.pin_input.setFocus()
