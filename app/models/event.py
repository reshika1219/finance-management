from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from app.utils.currency import parse_currency


@dataclass
class Event:
    id: Optional[int] = None
    event_name: str = ""
    event_date: str = ""  # ISO format YYYY-MM-DD
    client_name: str = ""
    location: str = ""
    description: str = ""
    income: Decimal = Decimal("0.00")
    employee_salary: Decimal = Decimal("0.00")
    employee_salary_note: str = ""
    transportation: Decimal = Decimal("0.00")
    transportation_note: str = ""
    food: Decimal = Decimal("0.00")
    food_note: str = ""
    supplier_payments: Decimal = Decimal("0.00")
    supplier_note: str = ""
    utilities_others: Decimal = Decimal("0.00")
    utilities_others_note: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @property
    def total_expenditure(self) -> Decimal:
        """Calculates total event expenditure from five expense categories."""
        return (
            parse_currency(self.employee_salary) +
            parse_currency(self.transportation) +
            parse_currency(self.food) +
            parse_currency(self.supplier_payments) +
            parse_currency(self.utilities_others)
        )

    @property
    def profit(self) -> Decimal:
        """Calculates net event profit: Income - Total Expenditure."""
        return parse_currency(self.income) - self.total_expenditure
