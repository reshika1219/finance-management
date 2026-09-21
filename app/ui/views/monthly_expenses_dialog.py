from decimal import Decimal
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from app.models.monthly_expense import MonthlyExpense
from app.services.monthly_service import get_monthly_expense, save_monthly_expense
from app.utils.currency import parse_currency, format_currency
from app.utils.date_utils import get_month_year_display


class MonthlyExpensesDialog(QDialog):
    def __init__(self, year: int, month: int, db_path: str = None, parent=None):
        super().__init__(parent)
        self.year = year
        self.month = month
        self.db_path = db_path
        self.expense_data = get_monthly_expense(self.year, self.month, self.db_path)

        self.setWindowTitle(f"Monthly Expenses — {get_month_year_display(self.year, self.month)}")
        self.setFixedSize(450, 520)

        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        title = QLabel(f"Monthly Expenses")
        title.setProperty("class", "page-title")
        layout.addWidget(title)

        subtitle = QLabel(get_month_year_display(self.year, self.month))
        subtitle.setStyleSheet("font-size: 16px; font-weight: 600; color: #0284C7;")
        layout.addWidget(subtitle)

        layout.addSpacing(6)

        # Expense Form Inputs
        self.rent_input = self._add_input_row(layout, "Rent (Rs.)")
        self.elec_input = self._add_input_row(layout, "Electricity Bill (Rs.)")
        self.water_input = self._add_input_row(layout, "Water Bill (Rs.)")
        self.phone_input = self._add_input_row(layout, "Telephone Bill (Rs.)")
        self.others_input = self._add_input_row(layout, "Others (Rs.)")

        layout.addStretch()

        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setProperty("class", "secondary-btn")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save Expenses")
        save_btn.setProperty("class", "primary-btn")
        save_btn.clicked.connect(self.on_save)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

    def _add_input_row(self, layout: QVBoxLayout, label_text: str) -> QLineEdit:
        lbl = QLabel(label_text)
        lbl.setStyleSheet("font-weight: 500; color: #334155;")
        layout.addWidget(lbl)

        inp = QLineEdit()
        inp.setPlaceholderText("0.00")
        layout.addWidget(inp)
        return inp

    def load_data(self):
        e = self.expense_data
        self.rent_input.setText(str(e.rent) if e.rent > 0 else "")
        self.elec_input.setText(str(e.electricity) if e.electricity > 0 else "")
        self.water_input.setText(str(e.water) if e.water > 0 else "")
        self.phone_input.setText(str(e.telephone) if e.telephone > 0 else "")
        self.others_input.setText(str(e.others) if e.others > 0 else "")

    def on_save(self):
        try:
            rent = parse_currency(self.rent_input.text())
            elec = parse_currency(self.elec_input.text())
            water = parse_currency(self.water_input.text())
            phone = parse_currency(self.phone_input.text())
            others = parse_currency(self.others_input.text())
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Please enter valid numeric amounts for all expenses.")
            return

        self.expense_data.rent = rent
        self.expense_data.electricity = elec
        self.expense_data.water = water
        self.expense_data.telephone = phone
        self.expense_data.others = others

        try:
            save_monthly_expense(self.expense_data, self.db_path)
            QMessageBox.information(
                self,
                "Expenses Saved",
                f"Monthly expenses for {get_month_year_display(self.year, self.month)} saved successfully."
            )
            self.accept()
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Could not save monthly expenses: {str(ex)}")
