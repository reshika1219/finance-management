from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from app.services.monthly_service import get_monthly_totals
from app.services.settings_service import get_settings
from app.utils.currency import format_currency
from app.utils.date_utils import get_month_year_display, get_previous_month, get_next_month
from app.ui.views.monthly_expenses_dialog import MonthlyExpensesDialog


class MonthlySummaryView(QWidget):
    export_month_excel = Signal(int, int)

    def __init__(self, db_path: str = None, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        today = datetime.now()
        self.current_year = today.year
        self.current_month = today.month

        self.init_ui()
        self.refresh_data()

    def set_active_month(self, year: int, month: int):
        self.current_year = year
        self.current_month = month
        self.refresh_data()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header Bar
        top_bar = QHBoxLayout()
        settings = get_settings(self.db_path)
        title_label = QLabel("Monthly Summary")
        title_label.setProperty("class", "page-title")
        top_bar.addWidget(title_label)

        top_bar.addStretch()

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

        # Number of Events
        self.events_count_lbl = QLabel("Number of Events: 0")
        self.events_count_lbl.setStyleSheet("font-size: 15px; font-weight: 600; color: #475569;")
        layout.addWidget(self.events_count_lbl)

        # 1. EVENT TOTALS CARD
        card_event = QFrame()
        card_event.setProperty("class", "card")
        cl1 = QVBoxLayout(card_event)
        cl1.setSpacing(10)

        t1 = QLabel("EVENT TOTALS")
        t1.setProperty("class", "card-title")
        cl1.addWidget(t1)

        self.lbl_ev_income = self._add_summary_row(cl1, "Total Event Income")
        self.lbl_ev_salary = self._add_summary_row(cl1, "Employee Salaries")
        self.lbl_ev_transport = self._add_summary_row(cl1, "Transportation")
        self.lbl_ev_food = self._add_summary_row(cl1, "Food for Employees")
        self.lbl_ev_supplier = self._add_summary_row(cl1, "Supplier Payments")
        self.lbl_ev_utilities = self._add_summary_row(cl1, "Utilities / Others")

        layout.addWidget(card_event)

        # 2. MONTHLY EXPENSES CARD
        card_monthly = QFrame()
        card_monthly.setProperty("class", "card")
        cl2 = QVBoxLayout(card_monthly)
        cl2.setSpacing(10)

        t2 = QLabel("MONTHLY EXPENSES")
        t2.setProperty("class", "card-title")
        cl2.addWidget(t2)

        self.lbl_gen_rent = self._add_summary_row(cl2, "Rent")
        self.lbl_gen_elec = self._add_summary_row(cl2, "Electricity")
        self.lbl_gen_water = self._add_summary_row(cl2, "Water")
        self.lbl_gen_phone = self._add_summary_row(cl2, "Telephone")
        self.lbl_gen_others = self._add_summary_row(cl2, "Others")

        layout.addWidget(card_monthly)

        # 3. FINAL SUMMARY CARD
        card_final = QFrame()
        card_final.setProperty("class", "card")
        card_final.setStyleSheet("background-color: #F8FAFC; border: 2px solid #0284C7;")
        cl3 = QVBoxLayout(card_final)
        cl3.setSpacing(10)

        t3 = QLabel("FINAL SUMMARY")
        t3.setProperty("class", "card-title")
        cl3.addWidget(t3)

        self.lbl_fin_income = self._add_summary_row(cl3, "Total Income", is_bold=True)
        self.lbl_fin_exp = self._add_summary_row(cl3, "Total Expenditure", is_bold=True)

        cl3.addSpacing(6)
        r_prof = QHBoxLayout()
        lbl_p = QLabel("Net Profit")
        lbl_p.setStyleSheet("font-size: 16px; font-weight: bold;")
        r_prof.addWidget(lbl_p)
        self.lbl_fin_profit = QLabel("Rs. 0.00")
        self.lbl_fin_profit.setStyleSheet("font-size: 18px; font-weight: bold; color: #0284C7;")
        r_prof.addWidget(self.lbl_fin_profit, 0, Qt.AlignRight)
        cl3.addLayout(r_prof)

        layout.addWidget(card_final)

        # Bottom Actions
        actions_layout = QHBoxLayout()

        self.edit_expenses_btn = QPushButton("Edit Monthly Expenses")
        self.edit_expenses_btn.setProperty("class", "secondary-btn")
        self.edit_expenses_btn.setCursor(Qt.PointingHandCursor)
        self.edit_expenses_btn.clicked.connect(self.on_edit_expenses)
        actions_layout.addWidget(self.edit_expenses_btn)

        self.export_excel_btn = QPushButton("Export Excel")
        self.export_excel_btn.setProperty("class", "primary-btn")
        self.export_excel_btn.setCursor(Qt.PointingHandCursor)
        self.export_excel_btn.clicked.connect(self.on_export_excel)
        actions_layout.addWidget(self.export_excel_btn)

        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _add_summary_row(self, layout: QVBoxLayout, label_text: str, is_bold: bool = False) -> QLabel:
        row = QHBoxLayout()
        lbl_name = QLabel(label_text)
        if is_bold:
            lbl_name.setStyleSheet("font-weight: bold;")
        row.addWidget(lbl_name)

        lbl_val = QLabel("Rs. 0.00")
        if is_bold:
            lbl_val.setStyleSheet("font-weight: bold;")
        row.addWidget(lbl_val, 0, Qt.AlignRight)

        layout.addLayout(row)
        return lbl_val

    def refresh_data(self):
        self.month_label.setText(get_month_year_display(self.current_year, self.current_month))
        t = get_monthly_totals(self.current_year, self.current_month, self.db_path)

        self.events_count_lbl.setText(f"Number of Events: {t.events_count}")

        # Event totals
        self.lbl_ev_income.setText(format_currency(t.total_income))
        self.lbl_ev_salary.setText(format_currency(t.employee_salaries))
        self.lbl_ev_transport.setText(format_currency(t.transportation))
        self.lbl_ev_food.setText(format_currency(t.food))
        self.lbl_ev_supplier.setText(format_currency(t.supplier_payments))
        self.lbl_ev_utilities.setText(format_currency(t.utilities_others))

        # Monthly General Expenses
        self.lbl_gen_rent.setText(format_currency(t.rent))
        self.lbl_gen_elec.setText(format_currency(t.electricity))
        self.lbl_gen_water.setText(format_currency(t.water))
        self.lbl_gen_phone.setText(format_currency(t.telephone))
        self.lbl_gen_others.setText(format_currency(t.monthly_others))

        # Final Summary
        self.lbl_fin_income.setText(format_currency(t.total_income))
        self.lbl_fin_exp.setText(format_currency(t.total_expenditure))
        self.lbl_fin_profit.setText(format_currency(t.net_profit))

        if t.net_profit < 0:
            self.lbl_fin_profit.setStyleSheet("font-size: 18px; font-weight: bold; color: #E11D48;")
        else:
            self.lbl_fin_profit.setStyleSheet("font-size: 18px; font-weight: bold; color: #0D9488;")

    def on_prev_month(self):
        self.current_year, self.current_month = get_previous_month(self.current_year, self.current_month)
        self.refresh_data()

    def on_next_month(self):
        self.current_year, self.current_month = get_next_month(self.current_year, self.current_month)
        self.refresh_data()

    def on_edit_expenses(self):
        dialog = MonthlyExpensesDialog(self.current_year, self.current_month, db_path=self.db_path, parent=self)
        if dialog.exec() == MonthlyExpensesDialog.Accepted:
            self.refresh_data()

    def on_export_excel(self):
        self.export_month_excel.emit(self.current_year, self.current_month)
