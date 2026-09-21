from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from app.services.backup_service import create_backup, restore_backup, validate_backup_file


class BackupView(QWidget):
    data_restored = Signal()

    def __init__(self, db_path: str = None, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Title
        title = QLabel("Backup & Restore")
        title.setProperty("class", "page-title")
        layout.addWidget(title)

        # Card 1: Create Backup
        card1 = QFrame()
        card1.setProperty("class", "card")
        l1 = QVBoxLayout(card1)
        l1.setSpacing(12)

        t1 = QLabel("CREATE BACKUP")
        t1.setProperty("class", "card-title")
        l1.addWidget(t1)

        d1 = QLabel("Export a complete backup of all events, monthly expenses, and settings into a single backup file.")
        d1.setProperty("class", "subtext")
        l1.addWidget(d1)

        b1_layout = QHBoxLayout()
        b1_layout.addStretch()
        self.create_btn = QPushButton("Create Backup")
        self.create_btn.setProperty("class", "primary-btn")
        self.create_btn.setCursor(Qt.PointingHandCursor)
        self.create_btn.clicked.connect(self.on_create_backup)
        b1_layout.addWidget(self.create_btn)
        l1.addLayout(b1_layout)

        layout.addWidget(card1)

        # Card 2: Restore Backup
        card2 = QFrame()
        card2.setProperty("class", "card")
        l2 = QVBoxLayout(card2)
        l2.setSpacing(12)

        t2 = QLabel("RESTORE BACKUP")
        t2.setProperty("class", "card-title")
        l2.addWidget(t2)

        d2 = QLabel("Restore your application data from a previously created backup file.")
        d2.setProperty("class", "subtext")
        l2.addWidget(d2)

        b2_layout = QHBoxLayout()
        b2_layout.addStretch()
        self.restore_btn = QPushButton("Restore Backup")
        self.restore_btn.setProperty("class", "danger-btn")
        self.restore_btn.setCursor(Qt.PointingHandCursor)
        self.restore_btn.clicked.connect(self.on_restore_backup)
        b2_layout.addWidget(self.restore_btn)
        l2.addLayout(b2_layout)

        layout.addWidget(card2)
        layout.addStretch()

    def on_create_backup(self):
        today_str = datetime.now().strftime("%Y-%m-%d")
        default_name = f"Chirathma_Flora_Backup_{today_str}.db"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Create Backup",
            default_name,
            "Database Backup (*.db)"
        )
        if file_path:
            try:
                create_backup(file_path, self.db_path)
                QMessageBox.information(
                    self,
                    "Backup Complete",
                    "The backup was created successfully."
                )
            except Exception as ex:
                QMessageBox.critical(self, "Backup Failed", f"Could not create backup: {str(ex)}")

    def on_restore_backup(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Backup File to Restore",
            "",
            "Database Backup (*.db)"
        )
        if not file_path:
            return

        if not validate_backup_file(file_path):
            QMessageBox.critical(
                self,
                "Invalid Backup",
                "The selected file could not be restored.\n\nIt does not appear to be a valid Chirathma Flora backup."
            )
            return

        # Confirmation Modal
        confirm = QMessageBox(self)
        confirm.setWindowTitle("Restore Backup?")
        confirm.setText("Restoring this backup will replace the current application data.\n\nWould you like to continue?")
        confirm.setIcon(QMessageBox.Warning)

        cancel_btn = confirm.addButton("Cancel", QMessageBox.RejectRole)
        restore_btn = confirm.addButton("Restore", QMessageBox.AcceptRole)
        confirm.setDefaultButton(cancel_btn)

        confirm.exec()
        if confirm.clickedButton() == restore_btn:
            try:
                restore_backup(file_path, self.db_path)
                QMessageBox.information(
                    self,
                    "Restore Complete",
                    "The application data has been restored successfully."
                )
                self.data_restored.emit()
            except Exception as ex:
                QMessageBox.critical(self, "Restore Failed", f"Could not restore backup: {str(ex)}")
