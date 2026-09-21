from decimal import Decimal
from datetime import date
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QDateEdit, QMessageBox, QFrame, QScrollArea, QWidget
)
from PySide6.QtCore import Qt, QDate
from app.models.event import Event
from app.services.event_service import save_event, calculate_event_expenditure, calculate_event_profit
from app.utils.currency import parse_currency, format_currency
from app.utils.date_utils import parse_iso_date, format_iso_date, DISPLAY_DATE_FORMAT


class EventFormDialog(QDialog):
    def __init__(self, event: Event = None, db_path: str = None, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.event = event or Event()
        self.is_edit = self.event.id is not None
        self.is_modified = False

        self.setWindowTitle("Edit Event" if self.is_edit else "Add Event")
        self.resize(550, 720)
        self.setMinimumSize(480, 600)

        self.init_ui()
        if self.is_edit:
            self.load_event_data()

        self.update_summary()
        self.is_modified = False  # Reset dirty flag after loading

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll Area container for smaller laptop screens
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Title Header
        header = QLabel("Edit Event" if self.is_edit else "Add Event")
        header.setProperty("class", "page-title")
        layout.addWidget(header)

        # 1. EVENT DETAILS SECTION
        sec1 = QLabel("EVENT DETAILS")
        sec1.setProperty("class", "section-title")
        layout.addWidget(sec1)

        layout.addWidget(QLabel("Event Name *"))
        self.event_name_input = QLineEdit()
        self.event_name_input.setPlaceholderText("e.g. Perera Wedding")
        self.event_name_input.textChanged.connect(self.on_changed)
        layout.addWidget(self.event_name_input)

        layout.addWidget(QLabel("Date * (DD/MM/YYYY)"))
        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.dateChanged.connect(self.on_changed)
        layout.addWidget(self.date_edit)

        layout.addWidget(QLabel("Client Name *"))
        self.client_name_input = QLineEdit()
        self.client_name_input.setPlaceholderText("e.g. Mr. Perera")
        self.client_name_input.textChanged.connect(self.on_changed)
        layout.addWidget(self.client_name_input)

        layout.addWidget(QLabel("Location"))
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("e.g. Kandy")
        self.location_input.textChanged.connect(self.on_changed)
        layout.addWidget(self.location_input)

        layout.addWidget(QLabel("Description"))
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("e.g. Wedding decoration")
        self.desc_input.textChanged.connect(self.on_changed)
        layout.addWidget(self.desc_input)

        # 2. INCOME SECTION
        sec2 = QLabel("INCOME")
        sec2.setProperty("class", "section-title")
        layout.addWidget(sec2)

        layout.addWidget(QLabel("Total Income (Rs.) *"))
        self.income_input = QLineEdit()
        self.income_input.setPlaceholderText("0.00")
        self.income_input.textChanged.connect(self.on_amount_changed)
        layout.addWidget(self.income_input)

        # 3. EVENT EXPENSES SECTION
        sec3 = QLabel("EVENT EXPENSES")
        sec3.setProperty("class", "section-title")
        layout.addWidget(sec3)

        # Expense rows (Salary, Transport, Food, Supplier, Utilities)
        self.salary_amt, self.salary_note = self._add_expense_row(layout, "Employee Salaries")
        self.transport_amt, self.transport_note = self._add_expense_row(layout, "Transportation")
        self.food_amt, self.food_note = self._add_expense_row(layout, "Food for Employees")
        self.supplier_amt, self.supplier_note = self._add_expense_row(layout, "Supplier Payments")
        self.utilities_amt, self.utilities_note = self._add_expense_row(layout, "Utilities / Others")

        # 4. SUMMARY CARD
        summary_card = QFrame()
        summary_card.setProperty("class", "card")
        summary_layout = QVBoxLayout(summary_card)

        summary_title = QLabel("SUMMARY")
        summary_title.setProperty("class", "card-title")
        summary_layout.addWidget(summary_title)

        r1 = QHBoxLayout()
        r1.addWidget(QLabel("Total Income:"))
        self.lbl_summary_income = QLabel("Rs. 0.00")
        self.lbl_summary_income.setStyleSheet("font-weight: bold;")
        r1.addWidget(self.lbl_summary_income, 0, Qt.AlignRight)
        summary_layout.addLayout(r1)

        r2 = QHBoxLayout()
        r2.addWidget(QLabel("Total Expenditure:"))
        self.lbl_summary_expenditure = QLabel("Rs. 0.00")
        self.lbl_summary_expenditure.setStyleSheet("font-weight: bold;")
        r2.addWidget(self.lbl_summary_expenditure, 0, Qt.AlignRight)
        summary_layout.addLayout(r2)

        summary_layout.addSpacing(6)

        r3 = QHBoxLayout()
        lbl_p = QLabel("Event Profit:")
        lbl_p.setStyleSheet("font-size: 16px; font-weight: bold;")
        r3.addWidget(lbl_p)
        self.lbl_summary_profit = QLabel("Rs. 0.00")
        self.lbl_summary_profit.setStyleSheet("font-size: 18px; font-weight: bold; color: #0284C7;")
        r3.addWidget(self.lbl_summary_profit, 0, Qt.AlignRight)
        summary_layout.addLayout(r3)

        layout.addWidget(summary_card)

        # 5. BUTTONS
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setProperty("class", "secondary-btn")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        self.save_btn = QPushButton("Save Event")
        self.save_btn.setProperty("class", "primary-btn")
        self.save_btn.clicked.connect(self.on_save)
        btn_layout.addWidget(self.save_btn)

        layout.addLayout(btn_layout)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _add_expense_row(self, layout: QVBoxLayout, label_text: str):
        lbl = QLabel(label_text)
        layout.addWidget(lbl)

        row = QHBoxLayout()
        amt_input = QLineEdit()
        amt_input.setPlaceholderText("Amount (Rs.)")
        amt_input.textChanged.connect(self.on_amount_changed)

        note_input = QLineEdit()
        note_input.setPlaceholderText("Optional note")
        note_input.textChanged.connect(self.on_changed)

        row.addWidget(amt_input, 2)
        row.addWidget(note_input, 3)
        layout.addLayout(row)

        return amt_input, note_input

    def on_changed(self):
        self.is_modified = True

    def on_amount_changed(self):
        self.is_modified = True
        self.update_summary()

    def update_summary(self):
        try:
            inc = parse_currency(self.income_input.text())
        except ValueError:
            inc = Decimal("0.00")

        try:
            exp = calculate_event_expenditure(
                self.salary_amt.text(),
                self.transport_amt.text(),
                self.food_amt.text(),
                self.supplier_amt.text(),
                self.utilities_amt.text(),
            )
        except ValueError:
            exp = Decimal("0.00")

        profit = calculate_event_profit(inc, exp)

        self.lbl_summary_income.setText(format_currency(inc))
        self.lbl_summary_expenditure.setText(format_currency(exp))
        self.lbl_summary_profit.setText(format_currency(profit))

        if profit < 0:
            self.lbl_summary_profit.setStyleSheet("font-size: 18px; font-weight: bold; color: #E11D48;")
        else:
            self.lbl_summary_profit.setStyleSheet("font-size: 18px; font-weight: bold; color: #0D9488;")

    def load_event_data(self):
        e = self.event
        self.event_name_input.setText(e.event_name)
        if e.event_date:
            d = parse_iso_date(e.event_date)
            self.date_edit.setDate(QDate(d.year, d.month, d.day))
        self.client_name_input.setText(e.client_name)
        self.location_input.setText(e.location)
        self.desc_input.setText(e.description)
        self.income_input.setText(str(e.income))

        self.salary_amt.setText(str(e.employee_salary) if e.employee_salary > 0 else "")
        self.salary_note.setText(e.employee_salary_note)

        self.transport_amt.setText(str(e.transportation) if e.transportation > 0 else "")
        self.transport_note.setText(e.transportation_note)

        self.food_amt.setText(str(e.food) if e.food > 0 else "")
        self.food_note.setText(e.food_note)

        self.supplier_amt.setText(str(e.supplier_payments) if e.supplier_payments > 0 else "")
        self.supplier_note.setText(e.supplier_note)

        self.utilities_amt.setText(str(e.utilities_others) if e.utilities_others > 0 else "")
        self.utilities_note.setText(e.utilities_others_note)

    def on_save(self):
        # Validation
        name = self.event_name_input.text().strip()
        client = self.client_name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Please enter the Event Name.")
            self.event_name_input.setFocus()
            return

        if not client:
            QMessageBox.warning(self, "Validation Error", "Please enter the Client Name.")
            self.client_name_input.setFocus()
            return

        try:
            income = parse_currency(self.income_input.text())
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid numeric Total Income.")
            self.income_input.setFocus()
            return

        try:
            salary = parse_currency(self.salary_amt.text())
            transport = parse_currency(self.transport_amt.text())
            food = parse_currency(self.food_amt.text())
            supplier = parse_currency(self.supplier_amt.text())
            utilities = parse_currency(self.utilities_amt.text())
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Please enter valid numeric expense amounts.")
            return

        qd = self.date_edit.date()
        iso_date = f"{qd.year():04d}-{qd.month():02d}-{qd.day():02d}"

        self.event.event_name = name
        self.event.event_date = iso_date
        self.event.client_name = client
        self.event.location = self.location_input.text().strip()
        self.event.description = self.desc_input.text().strip()
        self.event.income = income
        self.event.employee_salary = salary
        self.event.employee_salary_note = self.salary_note.text().strip()
        self.event.transportation = transport
        self.event.transportation_note = self.transport_note.text().strip()
        self.event.food = food
        self.event.food_note = self.food_note.text().strip()
        self.event.supplier_payments = supplier
        self.event.supplier_note = self.supplier_note.text().strip()
        self.event.utilities_others = utilities
        self.event.utilities_others_note = self.utilities_note.text().strip()

        try:
            save_event(self.event, self.db_path)
            QMessageBox.information(
                self,
                "Event Saved",
                "The event has been saved successfully."
            )
            self.accept()
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Could not save event: {str(ex)}")

    def closeEvent(self, event):
        if self.is_modified:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes.\nDo you want to discard them?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
