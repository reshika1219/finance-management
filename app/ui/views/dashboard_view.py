from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout
)
from PySide6.QtCore import Qt, Signal
from app.services.monthly_service import get_monthly_totals
from app.services.settings_service import get_settings
from app.utils.currency import format_currency
from app.utils.date_utils import get_month_year_display, get_previous_month, get_next_month
from app.ui.views.event_form_dialog import EventFormDialog
from app.ui.views.monthly_expenses_dialog import MonthlyExpensesDialog


class DashboardView(QWidget):
    navigate_to_events = Signal()
    navigate_to_monthly_summary = Signal(int, int)  # year, month
    export_month_excel = Signal(int, int)  # year, month

    def __init__(self, db_path: str = None, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        today = datetime.now()
        self.current_year = today.year
        self.current_month = today.month

        self.init_ui()
        self.refresh_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Business Name & Month Header
        top_bar = QHBoxLayout()
        settings = get_settings(self.db_path)
        title_label = QLabel(settings.business_name)
        title_label.setProperty("class", "page-title")
        top_bar.addWidget(title_label)

        top_bar.addStretch()

        # Month Selector Navigation Controls: < Previous Month  Current Month  Next Month >
        self.prev_btn = QPushButton("‹")
        self.prev_btn.setFixedSize(36, 36)
        self.prev_btn.setProperty("class", "icon-btn")
        self.prev_btn.setCursor(Qt.PointingHandCursor)
        self.prev_btn.clicked.connect(self.on_prev_month)
        top_bar.addWidget(self.prev_btn)

        self.month_label = QLabel()
        self.month_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #1E293B; min-width: 160px;")
        self.month_label.setAlignment(Qt.AlignCenter)
        top_bar.addWidget(self.month_label)

        self.next_btn = QPushButton("›")
        self.next_btn.setFixedSize(36, 36)
        self.next_btn.setProperty("class", "icon-btn")
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.clicked.connect(self.on_next_month)
        top_bar.addWidget(self.next_btn)

        layout.addLayout(top_bar)

        # Stat Cards Grid (2x2)
        grid = QGridLayout()
        grid.setSpacing(16)

        # 1. Events Card
        self.card_events = self._create_stat_card("Events", "0")
        grid.addWidget(self.card_events["frame"], 0, 0)

        # 2. Total Income Card
        self.card_income = self._create_stat_card("Total Income", "Rs. 0.00")
        grid.addWidget(self.card_income["frame"], 0, 1)

        # 3. Total Expenditure Card
        self.card_expenditure = self._create_stat_card("Total Expenditure", "Rs. 0.00")
        grid.addWidget(self.card_expenditure["frame"], 1, 0)

        # 4. Profit Card
        self.card_profit = self._create_stat_card("Profit", "Rs. 0.00", is_profit=True)
        grid.addWidget(self.card_profit["frame"], 1, 1)

        layout.addLayout(grid)

        layout.addSpacing(10)

        # Quick Actions Section
        sec_title = QLabel("Quick Actions")
        sec_title.setProperty("class", "section-title")
        layout.addWidget(sec_title)

        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)

        self.add_event_btn = QPushButton("+ Add Event")
        self.add_event_btn.setProperty("class", "primary-btn")
        self.add_event_btn.setCursor(Qt.PointingHandCursor)
        self.add_event_btn.clicked.connect(self.on_add_event)
        actions_layout.addWidget(self.add_event_btn)

        self.monthly_exp_btn = QPushButton("Monthly Expenses")
        self.monthly_exp_btn.setProperty("class", "secondary-btn")
        self.monthly_exp_btn.setCursor(Qt.PointingHandCursor)
        self.monthly_exp_btn.clicked.connect(self.on_monthly_expenses)
        actions_layout.addWidget(self.monthly_exp_btn)

        self.view_summary_btn = QPushButton("View Monthly Summary")
        self.view_summary_btn.setProperty("class", "secondary-btn")
        self.view_summary_btn.setCursor(Qt.PointingHandCursor)
        self.view_summary_btn.clicked.connect(self.on_view_summary)
        actions_layout.addWidget(self.view_summary_btn)

        self.export_month_btn = QPushButton("Export Month")
        self.export_month_btn.setProperty("class", "secondary-btn")
        self.export_month_btn.setCursor(Qt.PointingHandCursor)
        self.export_month_btn.clicked.connect(self.on_export_month)
        actions_layout.addWidget(self.export_month_btn)

        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        layout.addStretch()

    def _create_stat_card(self, title: str, default_val: str, is_profit: bool = False) -> dict:
        frame = QFrame()
        frame.setProperty("class", "card")
        l = QVBoxLayout(frame)
        l.setContentsMargins(18, 18, 18, 18)
        l.setSpacing(8)

        t_lbl = QLabel(title)
        t_lbl.setProperty("class", "card-title")
        l.addWidget(t_lbl)

        v_lbl = QLabel(default_val)
        v_lbl.setProperty("class", "card-value")
        l.addWidget(v_lbl)

        return {"frame": frame, "title_lbl": t_lbl, "val_lbl": v_lbl, "is_profit": is_profit}

    def refresh_data(self):
        self.month_label.setText(get_month_year_display(self.current_year, self.current_month))
        totals = get_monthly_totals(self.current_year, self.current_month, self.db_path)

        self.card_events["val_lbl"].setText(str(totals.events_count))
        self.card_income["val_lbl"].setText(format_currency(totals.total_income))
        self.card_expenditure["val_lbl"].setText(format_currency(totals.total_expenditure))

        profit_str = format_currency(totals.net_profit)
        self.card_profit["val_lbl"].setText(profit_str)

        if totals.net_profit < 0:
            self.card_profit["val_lbl"].setProperty("class", "card-value-negative")
        else:
            self.card_profit["val_lbl"].setProperty("class", "card-value-positive")

        self.card_profit["val_lbl"].style().unpolish(self.card_profit["val_lbl"])
        self.card_profit["val_lbl"].style().polish(self.card_profit["val_lbl"])

    def on_prev_month(self):
        self.current_year, self.current_month = get_previous_month(self.current_year, self.current_month)
        self.refresh_data()

    def on_next_month(self):
        self.current_year, self.current_month = get_next_month(self.current_year, self.current_month)
        self.refresh_data()

    def on_add_event(self):
        dialog = EventFormDialog(db_path=self.db_path, parent=self)
        if dialog.exec() == EventFormDialog.Accepted:
            self.refresh_data()

    def on_monthly_expenses(self):
        dialog = MonthlyExpensesDialog(self.current_year, self.current_month, db_path=self.db_path, parent=self)
        if dialog.exec() == MonthlyExpensesDialog.Accepted:
            self.refresh_data()

    def on_view_summary(self):
        self.navigate_to_monthly_summary.emit(self.current_year, self.current_month)

    def on_export_month(self):
        self.export_month_excel.emit(self.current_year, self.current_month)
