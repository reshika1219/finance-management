import pytest
from PySide6.QtWidgets import QApplication
import sys
from app.database.schema import init_db

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app

def test_event_form_dialog_instantiation(qapp, tmp_path):
    from app.ui.views.event_form_dialog import EventFormDialog

    db_file = str(tmp_path / "test_ui.db")
    init_db(db_file)

    dialog = EventFormDialog(db_path=db_file)
    assert dialog.windowTitle() == "Add Event"
    assert dialog.event_item is not None
    assert dialog.event_item.id is None

def test_monthly_expenses_dialog_instantiation(qapp, tmp_path):
    from app.ui.views.monthly_expenses_dialog import MonthlyExpensesDialog

    db_file = str(tmp_path / "test_ui.db")
    init_db(db_file)

    dialog = MonthlyExpensesDialog(year=2026, month=9, db_path=db_file)
    assert "Monthly Expenses" in dialog.windowTitle()
