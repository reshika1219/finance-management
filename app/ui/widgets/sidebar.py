from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QButtonGroup
from PySide6.QtCore import Qt, Signal
from app.services.settings_service import get_settings


class Sidebar(QWidget):
    navigation_changed = Signal(int)  # Page index (0 to 5)

    def __init__(self, db_path: str = None, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.setObjectName("sidebar")
        self.setFixedWidth(220)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 20, 12, 20)
        layout.setSpacing(8)

        # Header Title
        settings = get_settings(self.db_path)
        self.header = QLabel(settings.business_name)
        self.header.setObjectName("sidebarHeader")
        self.header.setWordWrap(True)
        layout.addWidget(self.header)

        layout.addSpacing(16)

        # Navigation Buttons
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        nav_items = [
            ("Dashboard", 0),
            ("Events", 1),
            ("Monthly Summary", 2),
            ("Reports", 3),
            ("Backup & Restore", 4),
            ("Settings", 5),
        ]

        self.buttons = []
        for text, index in nav_items:
            btn = QPushButton(text)
            btn.setProperty("class", "nav-btn")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            if index == 0:
                btn.setChecked(True)

            self.btn_group.addButton(btn, index)
            layout.addWidget(btn)
            self.buttons.append(btn)

        self.btn_group.idClicked.connect(self.on_nav_clicked)

        layout.addStretch()

    def on_nav_clicked(self, index: int):
        self.navigation_changed.emit(index)

    def set_active_index(self, index: int):
        btn = self.btn_group.button(index)
        if btn:
            btn.setChecked(True)
            self.navigation_changed.emit(index)

    def refresh_header(self):
        settings = get_settings(self.db_path)
        self.header.setText(settings.business_name)
