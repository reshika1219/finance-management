from decimal import Decimal
from dataclasses import dataclass
from app.services.monthly_service import get_monthly_totals, MonthlyTotals
from app.utils.date_utils import get_month_range_tuples, get_month_year_display


@dataclass
class MonthReportRow:
    year: int
    month: int
    month_name: str
    total_income: Decimal
    total_expenditure: Decimal
    profit: Decimal


@dataclass
class CombinedReport:
    period_label: str
    rows: list[MonthReportRow]
    total_income: Decimal
    total_expenditure: Decimal
    total_profit: Decimal


def get_combined_report_from_db(
    start_year: int, start_month: int, end_year: int, end_month: int, db_path: str = None
) -> CombinedReport:
    """Generates a combined multi-month financial report from saved SQLite data."""
    month_tuples = get_month_range_tuples(start_year, start_month, end_year, end_month)

    rows = []
    grand_income = Decimal("0.00")
    grand_expenditure = Decimal("0.00")
    grand_profit = Decimal("0.00")

    for y, m in month_tuples:
        mt = get_monthly_totals(y, m, db_path)
        m_name = get_month_year_display(y, m)
        row = MonthReportRow(
            year=y,
            month=m,
            month_name=m_name,
            total_income=mt.total_income,
            total_expenditure=mt.total_expenditure,
            profit=mt.net_profit,
        )
        rows.append(row)
        grand_income += mt.total_income
        grand_expenditure += mt.total_expenditure
        grand_profit += mt.net_profit

    start_label = get_month_year_display(start_year, start_month)
    end_label = get_month_year_display(end_year, end_month)
    if start_year == end_year and start_month == end_month:
        period_label = start_label
    else:
        period_label = f"{start_label} – {end_label}"

    return CombinedReport(
        period_label=period_label,
        rows=rows,
        total_income=grand_income,
        total_expenditure=grand_expenditure,
        total_profit=grand_profit,
    )
