from decimal import Decimal
import pytest
from app.services.event_service import calculate_event_expenditure, calculate_event_profit
from app.services.monthly_service import (
    calculate_month_general_expenses,
    calculate_month_total_expenditure,
    calculate_month_profit
)
from app.utils.currency import parse_currency, format_currency


def test_event_calculations():
    # Spec example (Section 48)
    income = "100000"
    salary = "10000"
    transport = "5000"
    food = "2500"
    supplier = "20000"
    utilities = "2500"

    expenditure = calculate_event_expenditure(salary, transport, food, supplier, utilities)
    assert expenditure == Decimal("40000.00")

    profit = calculate_event_profit(income, expenditure)
    assert profit == Decimal("60000.00")


def test_decimal_currency_precision():
    # Decimal precision check (1234.56 + 0.01)
    val1 = parse_currency("1234.56")
    val2 = parse_currency("0.01")
    assert val1 + val2 == Decimal("1234.57")

    fmt = format_currency(Decimal("1234.56"))
    assert fmt == "Rs. 1,234.56"


def test_negative_monthly_profit():
    # Zero income, high expenses -> negative profit
    income = "0.00"
    event_exp = "15000.00"
    gen_exp = calculate_month_general_expenses("50000", "12500", "3000", "4500", "5000") # 75,000
    assert gen_exp == Decimal("75000.00")

    total_exp = calculate_month_total_expenditure(event_exp, gen_exp) # 90,000
    assert total_exp == Decimal("90000.00")

    net_profit = calculate_month_profit(income, total_exp)
    assert net_profit == Decimal("-90000.00")
    assert format_currency(net_profit) == "-Rs. 90,000.00"
