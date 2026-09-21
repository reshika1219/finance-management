from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt, Signal
from app.models.event import Event
from app.services.event_service import get_all_events, delete_event
from app.ui.views.event_form_dialog import EventFormDialog
from app.utils.currency import format_currency
from app.utils.date_utils import format_display_date


class EventsView(QWidget):
    event_changed = Signal()

    def __init__(self, db_path: str = None, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.events_list: list[Event] = []

        self.init_ui()
        self.load_events()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header Row
        header_layout = QHBoxLayout()
        title_label = QLabel("Events")
        title_label.setProperty("class", "page-title")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        self.add_event_btn = QPushButton("+ Add Event")
        self.add_event_btn.setProperty("class", "primary-btn")
        self.add_event_btn.setCursor(Qt.PointingHandCursor)
        self.add_event_btn.clicked.connect(self.on_add_event)
        header_layout.addWidget(self.add_event_btn)

        layout.addLayout(header_layout)

        # Search & Filter Row
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by event, client, or location...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self.load_events)
        filter_layout.addWidget(self.search_input)

        layout.addLayout(filter_layout)

        # Events Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Date", "Event", "Client", "Location", "Income", "Expenditure", "Profit", "Actions"
        ])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)

        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)

    def load_events(self):
        query = self.search_input.text().strip()
        self.events_list = get_all_events(query, self.db_path)

        self.table.setRowCount(0)
        for row_idx, ev in enumerate(self.events_list):
            self.table.insertRow(row_idx)

            # Date
            item_date = QTableWidgetItem(format_display_date(ev.event_date))
            item_date.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 0, item_date)

            # Event Name
            item_name = QTableWidgetItem(ev.event_name)
            item_name.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row_idx, 1, item_name)

            # Client Name
            item_client = QTableWidgetItem(ev.client_name)
            item_client.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row_idx, 2, item_client)

            # Location
            item_loc = QTableWidgetItem(ev.location or "—")
            item_loc.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row_idx, 3, item_loc)

            # Income
            item_inc = QTableWidgetItem(format_currency(ev.income))
            item_inc.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 4, item_inc)

            # Expenditure
            item_exp = QTableWidgetItem(format_currency(ev.total_expenditure))
            item_exp.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 5, item_exp)

            # Profit
            item_prof = QTableWidgetItem(format_currency(ev.profit))
            item_prof.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if ev.profit < 0:
                item_prof.setForeground(Qt.red)
            else:
                item_prof.setForeground(Qt.darkGreen)
            self.table.setItem(row_idx, 6, item_prof)

            # Actions Cell
            actions_widget = QWidget()
            act_layout = QHBoxLayout(actions_widget)
            act_layout.setContentsMargins(4, 2, 4, 2)
            act_layout.setSpacing(6)

            edit_btn = QPushButton("Edit")
            edit_btn.setProperty("class", "secondary-btn")
            edit_btn.setStyleSheet("padding: 4px 10px; font-size: 12px;")
            edit_btn.clicked.connect(lambda _, e=ev: self.on_edit_event(e))
            act_layout.addWidget(edit_btn)

            del_btn = QPushButton("Delete")
            del_btn.setProperty("class", "danger-btn")
            del_btn.setStyleSheet("padding: 4px 10px; font-size: 12px;")
            del_btn.clicked.connect(lambda _, e=ev: self.on_delete_event(e))
            act_layout.addWidget(del_btn)

            self.table.setCellWidget(row_idx, 7, actions_widget)

    def on_add_event(self):
        dialog = EventFormDialog(db_path=self.db_path, parent=self)
        if dialog.exec() == EventFormDialog.Accepted:
            self.load_events()
            self.event_changed.emit()

    def on_edit_event(self, event: Event):
        dialog = EventFormDialog(event=event, db_path=self.db_path, parent=self)
        if dialog.exec() == EventFormDialog.Accepted:
            self.load_events()
            self.event_changed.emit()

    def on_delete_event(self, event: Event):
        confirm = QMessageBox(self)
        confirm.setWindowTitle("Delete Event?")
        confirm.setText(f'Are you sure you want to delete\n"{event.event_name}"?\n\nThis action cannot be undone.')
        confirm.setIcon(QMessageBox.Warning)
        
        cancel_btn = confirm.addButton("Cancel", QMessageBox.RejectRole)
        delete_btn = confirm.addButton("Delete", QMessageBox.AcceptRole)
        confirm.setDefaultButton(cancel_btn)

        confirm.exec()
        if confirm.clickedButton() == delete_btn:
            delete_event(event.id, self.db_path)
            self.load_events()
            self.event_changed.emit()
