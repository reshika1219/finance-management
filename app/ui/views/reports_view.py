from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSpinBox,
    QPushButton, QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QFileDialog, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt
from app.services.report_service import get_combined_report_from_db, CombinedReport
from app.reports.excel_importer import build_combined_report_from_files
from app.reports.excel_generator import generate_combined_excel
from app.utils.currency import format_currency
from app.utils.date_utils import MONTH_NAMES


class ReportsView(QWidget):
    def __init__(self, db_path: str = None, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.active_report: CombinedReport | None = None
        self.selected_file_paths: list[str] = []

        self.init_ui()

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

        # Page Title
        title = QLabel("Reports")
        title.setProperty("class", "page-title")
        layout.addWidget(title)

        # ----------------------------------------------------
        # OPTION 1: Generate Report from Saved Data
        # ----------------------------------------------------
        card1 = QFrame()
        card1.setProperty("class", "card")
        l1 = QVBoxLayout(card1)
        l1.setSpacing(12)

        t1 = QLabel("Generate Report from Saved Data")
        t1.setProperty("class", "card-title")
        l1.addWidget(t1)

        row_date = QHBoxLayout()
        row_date.setSpacing(16)

        # From
        row_date.addWidget(QLabel("From:"))
        self.start_month_cb = QComboBox()
        self.start_month_cb.addItems(MONTH_NAMES)
        self.start_month_cb.setCurrentIndex(0)  # Jan
        row_date.addWidget(self.start_month_cb)

        self.start_year_sb = QSpinBox()
        self.start_year_sb.setRange(2000, 2099)
        self.start_year_sb.setValue(datetime.now().year)
        row_date.addWidget(self.start_year_sb)

        row_date.addSpacing(20)

        # To
        row_date.addWidget(QLabel("To:"))
        self.end_month_cb = QComboBox()
        self.end_month_cb.addItems(MONTH_NAMES)
        self.end_month_cb.setCurrentIndex(datetime.now().month - 1)
        row_date.addWidget(self.end_month_cb)

        self.end_year_sb = QSpinBox()
        self.end_year_sb.setRange(2000, 2099)
        self.end_year_sb.setValue(datetime.now().year)
        row_date.addWidget(self.end_year_sb)

        row_date.addStretch()

        self.btn_gen_db = QPushButton("Generate Report")
        self.btn_gen_db.setProperty("class", "primary-btn")
        self.btn_gen_db.setCursor(Qt.PointingHandCursor)
        self.btn_gen_db.clicked.connect(self.on_generate_from_db)
        row_date.addWidget(self.btn_gen_db)

        l1.addLayout(row_date)
        layout.addWidget(card1)

        # ----------------------------------------------------
        # OPTION 2: Generate Report from Monthly Excel Files
        # ----------------------------------------------------
        card2 = QFrame()
        card2.setProperty("class", "card")
        l2 = QVBoxLayout(card2)
        l2.setSpacing(12)

        t2 = QLabel("Generate Report from Monthly Excel Files")
        t2.setProperty("class", "card-title")
        l2.addWidget(t2)

        row_files = QHBoxLayout()
        self.btn_select_files = QPushButton("Select Monthly Excel Files...")
        self.btn_select_files.setProperty("class", "secondary-btn")
        self.btn_select_files.setCursor(Qt.PointingHandCursor)
        self.btn_select_files.clicked.connect(self.on_select_files)
        row_files.addWidget(self.btn_select_files)

        self.lbl_selected_files = QLabel("No files selected")
        self.lbl_selected_files.setProperty("class", "subtext")
        row_files.addWidget(self.lbl_selected_files)

        row_files.addStretch()

        self.btn_gen_files = QPushButton("Generate Combined Report")
        self.btn_gen_files.setProperty("class", "primary-btn")
        self.btn_gen_files.setCursor(Qt.PointingHandCursor)
        self.btn_gen_files.clicked.connect(self.on_generate_from_files)
        row_files.addWidget(self.btn_gen_files)

        l2.addLayout(row_files)
        layout.addWidget(card2)

        # ----------------------------------------------------
        # REPORT PREVIEW TABLE & EXPORT
        # ----------------------------------------------------
        self.preview_card = QFrame()
        self.preview_card.setProperty("class", "card")
        self.preview_card.setVisible(False)
        lp = QVBoxLayout(self.preview_card)
        lp.setSpacing(12)

        self.lbl_report_period = QLabel("Reporting Period:")
        self.lbl_report_period.setStyleSheet("font-size: 16px; font-weight: bold; color: #0284C7;")
        lp.addWidget(self.lbl_report_period)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Month", "Total Income (Rs.)", "Total Expenditure (Rs.)", "Profit (Rs.)"
        ])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.table.verticalHeader().setVisible(False)
        lp.addWidget(self.table)

        row_export = QHBoxLayout()
        row_export.addStretch()
        self.btn_export = QPushButton("Export Combined Excel")
        self.btn_export.setProperty("class", "primary-btn")
        self.btn_export.setCursor(Qt.PointingHandCursor)
        self.btn_export.clicked.connect(self.on_export_combined_excel)
        row_export.addWidget(self.btn_export)
        lp.addLayout(row_export)

        layout.addWidget(self.preview_card)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def on_generate_from_db(self):
        s_m = self.start_month_cb.currentIndex() + 1
        s_y = self.start_year_sb.value()
        e_m = self.end_month_cb.currentIndex() + 1
        e_y = self.end_year_sb.value()

        if (s_y > e_y) or (s_y == e_y and s_m > e_m):
            QMessageBox.warning(self, "Invalid Date Range", "Start month/year must be prior to or equal to End month/year.")
            return

        try:
            report = get_combined_report_from_db(s_y, s_m, e_y, e_m, self.db_path)
            self.display_report(report)
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Could not generate report: {str(ex)}")

    def on_select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Monthly Excel Files",
            "",
            "Excel Files (*.xlsx)"
        )
        if files:
            self.selected_file_paths = files
            self.lbl_selected_files.setText(f"{len(files)} file(s) selected")
        else:
            self.selected_file_paths = []
            self.lbl_selected_files.setText("No files selected")

    def on_generate_from_files(self):
        if not self.selected_file_paths:
            QMessageBox.warning(self, "No Files Selected", "Please select one or more monthly Excel files first.")
            return

        try:
            report = build_combined_report_from_files(self.selected_file_paths)
            self.display_report(report)
        except ValueError as ve:
            QMessageBox.warning(self, "Import Error", str(ve))
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Could not import Excel files: {str(ex)}")

    def display_report(self, report: CombinedReport):
        self.active_report = report
        self.lbl_report_period.setText(f"Reporting Period: {report.period_label}")
        self.preview_card.setVisible(True)

        self.table.setRowCount(0)

        # Rows
        for row_idx, r in enumerate(report.rows):
            self.table.insertRow(row_idx)

            item_m = QTableWidgetItem(r.month_name)
            self.table.setItem(row_idx, 0, item_m)

            item_inc = QTableWidgetItem(format_currency(r.total_income))
            item_inc.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 1, item_inc)

            item_exp = QTableWidgetItem(format_currency(r.total_expenditure))
            item_exp.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 2, item_exp)

            item_prof = QTableWidgetItem(format_currency(r.profit))
            item_prof.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if r.profit < 0:
                item_prof.setForeground(Qt.GlobalColor.red)
            else:
                item_prof.setForeground(Qt.GlobalColor.darkGreen)
            self.table.setItem(row_idx, 3, item_prof)

        # Total Row
        tot_idx = self.table.rowCount()
        self.table.insertRow(tot_idx)

        item_tot_lbl = QTableWidgetItem("TOTAL")
        item_tot_lbl.setTextAlignment(Qt.AlignCenter)
        item_tot_lbl.setStyleSheet("font-weight: bold;")
        self.table.setItem(tot_idx, 0, item_tot_lbl)

        item_tot_inc = QTableWidgetItem(format_currency(report.total_income))
        item_tot_inc.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.table.setItem(tot_idx, 1, item_tot_inc)

        item_tot_exp = QTableWidgetItem(format_currency(report.total_expenditure))
        item_tot_exp.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.table.setItem(tot_idx, 2, item_tot_exp)

        item_tot_prof = QTableWidgetItem(format_currency(report.total_profit))
        item_tot_prof.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        if report.total_profit < 0:
            item_tot_prof.setForeground(Qt.GlobalColor.red)
        else:
            item_tot_prof.setForeground(Qt.GlobalColor.darkGreen)
        self.table.setItem(tot_idx, 3, item_tot_prof)

        # Style total row bold
        for c in range(4):
            font = self.table.item(tot_idx, c).font()
            font.setBold(True)
            self.table.item(tot_idx, c).setFont(font)

    def on_export_combined_excel(self):
        if not self.active_report:
            return

        default_filename = f"Chirathma_Flora_Report_{self.active_report.period_label.replace(' – ', '_to_').replace(' ', '_')}.xlsx"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Combined Excel Report",
            default_filename,
            "Excel Files (*.xlsx)"
        )
        if file_path:
            try:
                generate_combined_excel(self.active_report, file_path, self.db_path)
                QMessageBox.information(
                    self,
                    "Export Complete",
                    "The combined Excel report was created successfully."
                )
            except PermissionError:
                QMessageBox.critical(
                    self,
                    "Unable to Save Report",
                    "The Excel file may currently be open in another application.\n\nPlease close it and try again."
                )
            except Exception as ex:
                QMessageBox.critical(self, "Export Failed", f"Could not create Excel report: {str(ex)}")
