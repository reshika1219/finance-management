from decimal import Decimal
from dataclasses import dataclass
from app.database.connection import get_connection
from app.models.monthly_expense import MonthlyExpense
from app.models.event import Event
from app.services.event_service import get_events_by_month
from app.utils.currency import parse_currency


@dataclass
class MonthlyTotals:
    year: int
    month: int
    events_count: int
    total_income: Decimal
    total_event_expenditure: Decimal
    total_general_expenditure: Decimal
    total_expenditure: Decimal
    net_profit: Decimal
    # Detailed expense breakdown
    employee_salaries: Decimal
    transportation: Decimal
    food: Decimal
    supplier_payments: Decimal
    utilities_others: Decimal
    rent: Decimal
    electricity: Decimal
    water: Decimal
    telephone: Decimal
    monthly_others: Decimal


def calculate_month_general_expenses(
    rent: Decimal | str | float,
    electricity: Decimal | str | float,
    water: Decimal | str | float,
    telephone: Decimal | str | float,
    others: Decimal | str | float,
) -> Decimal:
    """Calculates general monthly expenditure sum."""
    return (
        parse_currency(rent)
        + parse_currency(electricity)
        + parse_currency(water)
        + parse_currency(telephone)
        + parse_currency(others)
    )


def calculate_month_total_expenditure(
    event_expenditure: Decimal | str | float,
    general_expenditure: Decimal | str | float,
) -> Decimal:
    """Calculates Total Monthly Expenditure: Event Expenditure + General Expenditure."""
    return parse_currency(event_expenditure) + parse_currency(general_expenditure)


def calculate_month_profit(
    total_income: Decimal | str | float,
    total_expenditure: Decimal | str | float,
) -> Decimal:
    """Calculates Monthly Net Profit: Total Monthly Income - Total Monthly Expenditure."""
    return parse_currency(total_income) - parse_currency(total_expenditure)


def get_monthly_expense(year: int, month: int, db_path: str = None) -> MonthlyExpense:
    """Fetches general monthly expenses for year/month, or returns a default 0.00 instance."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM monthly_expenses WHERE year = ? AND month = ?;",
            (year, month),
        )
        row = cursor.fetchone()
        if row:
            return MonthlyExpense(
                id=row["id"],
                year=row["year"],
                month=row["month"],
                rent=parse_currency(row["rent"]),
                electricity=parse_currency(row["electricity"]),
                water=parse_currency(row["water"]),
                telephone=parse_currency(row["telephone"]),
                others=parse_currency(row["others"]),
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
        return MonthlyExpense(year=year, month=month)
    finally:
        conn.close()


def save_monthly_expense(exp: MonthlyExpense, db_path: str = None) -> MonthlyExpense:
    """Saves or updates general monthly expenses for a given year/month."""
    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO monthly_expenses (year, month, rent, electricity, water, telephone, others, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(year, month) DO UPDATE SET
                    rent = excluded.rent,
                    electricity = excluded.electricity,
                    water = excluded.water,
                    telephone = excluded.telephone,
                    others = excluded.others,
                    updated_at = CURRENT_TIMESTAMP;
                """,
                (
                    exp.year,
                    exp.month,
                    str(parse_currency(exp.rent)),
                    str(parse_currency(exp.electricity)),
                    str(parse_currency(exp.water)),
                    str(parse_currency(exp.telephone)),
                    str(parse_currency(exp.others)),
                ),
            )
            if exp.id is None:
                cursor.execute(
                    "SELECT id FROM monthly_expenses WHERE year = ? AND month = ?;",
                    (exp.year, exp.month),
                )
                r = cursor.fetchone()
                if r:
                    exp.id = r["id"]
            return exp
    finally:
        conn.close()


def get_monthly_totals(year: int, month: int, db_path: str = None) -> MonthlyTotals:
    """Calculates all aggregated monthly financial metrics for the requested year and month."""
    events = get_events_by_month(year, month, db_path)
    gen_expenses = get_monthly_expense(year, month, db_path)

    total_income = Decimal("0.00")
    emp_salaries = Decimal("0.00")
    transport = Decimal("0.00")
    food = Decimal("0.00")
    suppliers = Decimal("0.00")
    util_others = Decimal("0.00")

    for ev in events:
        total_income += ev.income
        emp_salaries += ev.employee_salary
        transport += ev.transportation
        food += ev.food
        suppliers += ev.supplier_payments
        util_others += ev.utilities_others

    total_event_exp = emp_salaries + transport + food + suppliers + util_others
    total_gen_exp = gen_expenses.total_general_expenditure
    total_expenditure = total_event_exp + total_gen_exp
    net_profit = total_income - total_expenditure

    return MonthlyTotals(
        year=year,
        month=month,
        events_count=len(events),
        total_income=total_income,
        total_event_expenditure=total_event_exp,
        total_general_expenditure=total_gen_exp,
        total_expenditure=total_expenditure,
        net_profit=net_profit,
        employee_salaries=emp_salaries,
        transportation=transport,
        food=food,
        supplier_payments=suppliers,
        utilities_others=util_others,
        rent=gen_expenses.rent,
        electricity=gen_expenses.electricity,
        water=gen_expenses.water,
        telephone=gen_expenses.telephone,
        monthly_others=gen_expenses.others,
    )
