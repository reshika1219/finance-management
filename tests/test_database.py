import os
import tempfile
from decimal import Decimal
import pytest

from app.database.schema import init_db
from app.models.event import Event
from app.models.monthly_expense import MonthlyExpense
from app.services.event_service import save_event, get_event_by_id, delete_event, get_events_by_month
from app.services.monthly_service import save_monthly_expense, get_monthly_expense, get_monthly_totals
from app.services.auth_service import AuthService


@pytest.fixture
def temp_db():
    temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db_path = temp_file.name
    temp_file.close()
    init_db(db_path)
    yield db_path
    if os.path.exists(db_path):
        os.remove(db_path)


def test_pin_auth_flow(temp_db):
    auth = AuthService(temp_db)
    assert auth.is_first_launch() is True

    # Invalid PIN format
    with pytest.raises(ValueError):
        auth.setup_pin("123", "123")

    # Mismatching confirmation
    with pytest.raises(ValueError):
        auth.setup_pin("1234", "5678")

    # Valid PIN setup
    auth.setup_pin("1234", "1234")
    assert auth.is_first_launch() is False
    assert auth.verify("1234") is True
    assert auth.verify("9999") is False

    # Change PIN
    auth.change_pin("1234", "4321", "4321")
    assert auth.verify("1234") is False
    assert auth.verify("4321") is True


def test_event_crud(temp_db):
    ev = Event(
        event_name="Perera Wedding",
        event_date="2026-09-21",
        client_name="Mr. Perera",
        location="Kandy",
        description="Wedding decoration",
        income=Decimal("350000.00"),
        employee_salary=Decimal("45000.00"),
        transportation=Decimal("20000.00"),
        food=Decimal("12000.00"),
        supplier_payments=Decimal("125000.00"),
        utilities_others=Decimal("8000.00")
    )
    saved = save_event(ev, temp_db)
    assert saved.id is not None
    assert saved.profit == Decimal("140000.00")

    # Fetch
    fetched = get_event_by_id(saved.id, temp_db)
    assert fetched.event_name == "Perera Wedding"
    assert fetched.income == Decimal("350000.00")

    # Edit
    fetched.income = Decimal("400000.00")
    updated = save_event(fetched, temp_db)
    assert updated.profit == Decimal("190000.00")

    # Delete
    assert delete_event(saved.id, temp_db) is True
    assert get_event_by_id(saved.id, temp_db) is None


def test_monthly_totals_aggregator(temp_db):
    # Add two events in Sept 2026
    save_event(Event(
        event_name="Event A", event_date="2026-09-10", client_name="Client A",
        income=Decimal("500000.00"), employee_salary=Decimal("50000.00")
    ), temp_db)

    save_event(Event(
        event_name="Event B", event_date="2026-09-15", client_name="Client B",
        income=Decimal("750000.00"), supplier_payments=Decimal("350000.00")
    ), temp_db)

    # Add general monthly expenses
    save_monthly_expense(MonthlyExpense(
        year=2026, month=9, rent=Decimal("50000.00"), electricity=Decimal("12500.00"),
        water=Decimal("3000.00"), telephone=Decimal("4500.00"), others=Decimal("5000.00")
    ), temp_db)

    totals = get_monthly_totals(2026, 9, temp_db)
    assert totals.events_count == 2
    assert totals.total_income == Decimal("1250000.00")
    assert totals.total_event_expenditure == Decimal("400000.00")
    assert totals.total_general_expenditure == Decimal("75000.00")
    assert totals.total_expenditure == Decimal("475000.00")
    assert totals.net_profit == Decimal("775000.00")
