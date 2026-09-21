from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from app.utils.currency import parse_currency


@dataclass
class MonthlyExpense:
    id: Optional[int] = None
    year: int = 2026
    month: int = 1
    rent: Decimal = Decimal("0.00")
    electricity: Decimal = Decimal("0.00")
    water: Decimal = Decimal("0.00")
    telephone: Decimal = Decimal("0.00")
    others: Decimal = Decimal("0.00")
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @property
    def total_general_expenditure(self) -> Decimal:
        """Calculates total general monthly expenditure from the five categories."""
        return (
            parse_currency(self.rent) +
            parse_currency(self.electricity) +
            parse_currency(self.water) +
            parse_currency(self.telephone) +
            parse_currency(self.others)
        )
