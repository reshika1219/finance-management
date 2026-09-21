import sys
import os
from PySide6.QtWidgets import QApplication
from app.database.schema import init_db
from app.services.auth_service import AuthService
from app.ui.styles import MAIN_STYLE
from app.ui.views.pin_view import PinDialog
from app.ui.main_window import MainWindow


def main():
    # Initialize SQLite schema
    init_db()

    app = QApplication(sys.argv)
    app.setStyleSheet(MAIN_STYLE)

    auth_service = AuthService()

    # Show PIN dialog (Setup PIN on first run, Unlock PIN on subsequent runs)
    pin_dialog = PinDialog(auth_service)
    if pin_dialog.exec() == PinDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
