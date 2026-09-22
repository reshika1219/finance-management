import os
import tempfile
from decimal import Decimal
import pytest

from app.database.schema import init_db
from app.models.event import Event
from app.models.monthly_expense import MonthlyExpense
from app.services.event_service import save_event
from app.services.monthly_service import save_monthly_expense
from app.reports.excel_generator import generate_monthly_excel
from app.reports.excel_importer import read_monthly_excel_file, build_combined_report_from_files


@pytest.fixture
def temp_db_with_data():
    temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db_path = temp_file.name
    temp_file.close()
    init_db(db_path)

    save_event(Event(
        event_name="Wedding A", event_date="2026-09-05", client_name="Client A",
        income=Decimal("500000.00"), employee_salary=Decimal("50000.00")
    ), db_path)

    save_monthly_expense(MonthlyExpense(
        year=2026, month=9, rent=Decimal("50000.00")
    ), db_path)

    yield db_path

    if os.path.exists(db_path):
        os.remove(db_path)


def test_excel_export_import_roundtrip(temp_db_with_data):
    excel_file = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    excel_path = excel_file.name
    excel_file.close()

    try:
        generate_monthly_excel(2026, 9, excel_path, temp_db_with_data)
        assert os.path.exists(excel_path)

        # Re-import and check metadata
        imported_row = read_monthly_excel_file(excel_path)
        assert imported_row.year == 2026
        assert imported_row.month == 9
        assert imported_row.total_income == Decimal("500000.00")
        assert imported_row.total_expenditure == Decimal("100000.00")
        assert imported_row.profit == Decimal("400000.00")
    finally:
        if os.path.exists(excel_path):
            os.remove(excel_path)


def test_duplicate_reporting_month_rejection(temp_db_with_data):
    f1 = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False).name
    f2 = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False).name

    try:
        generate_monthly_excel(2026, 9, f1, temp_db_with_data)
        generate_monthly_excel(2026, 9, f2, temp_db_with_data)

        # Combining f1 and f2 should raise ValueError for duplicate month
        with pytest.raises(ValueError) as exc_info:
            build_combined_report_from_files([f1, f2])

        assert "Duplicate Month" in str(exc_info.value)
    finally:
        for f in (f1, f2):
            if os.path.exists(f):
                os.remove(f)


def test_invalid_format_version_rejection(temp_db_with_data):
    excel_file = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    excel_path = excel_file.name
    excel_file.close()

    try:
        generate_monthly_excel(2026, 9, excel_path, temp_db_with_data)
        import openpyxl
        wb = openpyxl.load_workbook(excel_path)
        ws_meta = wb["_ReportMetadata"]
        # Modify format_version to 2
        for row in ws_meta.iter_rows():
            if row[0].value == "format_version":
                row[1].value = "2"
        wb.save(excel_path)

        with pytest.raises(ValueError) as exc_info:
            read_monthly_excel_file(excel_path)

        assert "Unsupported report format version" in str(exc_info.value)
    finally:
        if os.path.exists(excel_path):
            os.remove(excel_path)
