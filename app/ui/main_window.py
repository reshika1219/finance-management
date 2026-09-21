from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QFileDialog, QMessageBox
from PySide6.QtCore import Qt
from app.services.settings_service import get_settings
from app.ui.widgets.sidebar import Sidebar
from app.ui.views.dashboard_view import DashboardView
from app.ui.views.events_view import EventsView
from app.ui.views.monthly_summary_view import MonthlySummaryView
from app.ui.views.reports_view import ReportsView
from app.ui.views.backup_view import BackupView
from app.ui.views.settings_view import SettingsView
from app.reports.excel_generator import generate_monthly_excel
from app.utils.date_utils import MONTH_NAMES


class MainWindow(QMainWindow):
    def __init__(self, db_path: str = None):
        super().__init__()
        self.db_path = db_path
        self.settings = get_settings(self.db_path)

        self.setWindowTitle(f"{self.settings.business_name} — Event Accounts")
        self.resize(1200, 750)
        self.setMinimumSize(1000, 650)

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left Sidebar
        self.sidebar = Sidebar(db_path=self.db_path)
        self.sidebar.navigation_changed.connect(self.on_navigation_changed)
        main_layout.addWidget(self.sidebar)

        # Right Content Stack
        self.stack = QStackedWidget()

        # 0: Dashboard View
        self.dashboard_view = DashboardView(db_path=self.db_path)
        self.dashboard_view.navigate_to_monthly_summary.connect(self.navigate_to_summary)
        self.dashboard_view.export_month_excel.connect(self.export_month_excel)
        self.stack.addWidget(self.dashboard_view)

        # 1: Events View
        self.events_view = EventsView(db_path=self.db_path)
        self.events_view.event_changed.connect(self.on_data_changed)
        self.stack.addWidget(self.events_view)

        # 2: Monthly Summary View
        self.monthly_summary_view = MonthlySummaryView(db_path=self.db_path)
        self.monthly_summary_view.export_month_excel.connect(self.export_month_excel)
        self.stack.addWidget(self.monthly_summary_view)

        # 3: Reports View
        self.reports_view = ReportsView(db_path=self.db_path)
        self.stack.addWidget(self.reports_view)

        # 4: Backup View
        self.backup_view = BackupView(db_path=self.db_path)
        self.backup_view.data_restored.connect(self.on_data_changed)
        self.stack.addWidget(self.backup_view)

        # 5: Settings View
        self.settings_view = SettingsView(db_path=self.db_path)
        self.settings_view.settings_changed.connect(self.update_business_title)
        self.stack.addWidget(self.settings_view)

        main_layout.addWidget(self.stack)
        self.setCentralWidget(main_widget)

    def on_navigation_changed(self, index: int):
        self.stack.setCurrentIndex(index)
        # Refresh current view data on navigation
        if index == 0:
            self.dashboard_view.refresh_data()
        elif index == 1:
            self.events_view.load_events()
        elif index == 2:
            self.monthly_summary_view.refresh_data()

    def navigate_to_summary(self, year: int, month: int):
        self.monthly_summary_view.set_active_month(year, month)
        self.sidebar.set_active_index(2)

    def on_data_changed(self):
        self.dashboard_view.refresh_data()
        self.monthly_summary_view.refresh_data()

    def export_month_excel(self, year: int, month: int):
        month_name = MONTH_NAMES[month - 1]
        default_filename = f"Chirathma_Flora_{month_name}_{year}.xlsx"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Monthly Excel",
            default_filename,
            "Excel Files (*.xlsx)"
        )
        if file_path:
            try:
                generate_monthly_excel(year, month, file_path, self.db_path)
                QMessageBox.information(
                    self,
                    "Export Complete",
                    "The Excel report was created successfully."
                )
            except PermissionError:
                QMessageBox.critical(
                    self,
                    "Unable to Save Report",
                    "The Excel file may currently be open in another application.\n\nPlease close it and try again."
                )
            except Exception as ex:
                QMessageBox.critical(self, "Export Failed", f"Could not create Excel file: {str(ex)}")

    def update_business_title(self):
        self.settings = get_settings(self.db_path)
        self.setWindowTitle(f"{self.settings.business_name} — Event Accounts")
        self.sidebar.refresh_header()

