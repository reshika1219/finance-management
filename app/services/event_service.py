from decimal import Decimal
from typing import Optional
from app.database.connection import get_connection
from app.models.event import Event
from app.utils.currency import parse_currency


def calculate_event_expenditure(
    employee_salary: Decimal | str | float,
    transportation: Decimal | str | float,
    food: Decimal | str | float,
    supplier_payments: Decimal | str | float,
    utilities_others: Decimal | str | float,
) -> Decimal:
    """Calculates total event expenditure from the five expense categories."""
    return (
        parse_currency(employee_salary)
        + parse_currency(transportation)
        + parse_currency(food)
        + parse_currency(supplier_payments)
        + parse_currency(utilities_others)
    )


def calculate_event_profit(
    income: Decimal | str | float,
    total_expenditure: Decimal | str | float,
) -> Decimal:
    """Calculates event profit: Total Income - Total Expenditure."""
    return parse_currency(income) - parse_currency(total_expenditure)


def row_to_event(row) -> Event:
    """Converts a SQLite sqlite3.Row object to an Event dataclass instance."""
    return Event(
        id=row["id"],
        event_name=row["event_name"],
        event_date=row["event_date"],
        client_name=row["client_name"],
        location=row["location"] or "",
        description=row["description"] or "",
        income=parse_currency(row["income"]),
        employee_salary=parse_currency(row["employee_salary"]),
        employee_salary_note=row["employee_salary_note"] or "",
        transportation=parse_currency(row["transportation"]),
        transportation_note=row["transportation_note"] or "",
        food=parse_currency(row["food"]),
        food_note=row["food_note"] or "",
        supplier_payments=parse_currency(row["supplier_payments"]),
        supplier_note=row["supplier_note"] or "",
        utilities_others=parse_currency(row["utilities_others"]),
        utilities_others_note=row["utilities_others_note"] or "",
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def save_event(event: Event, db_path: str = None) -> Event:
    """Saves a new or existing event into the database."""
    if not event.event_name.strip():
        raise ValueError("Event Name is required.")
    if not event.event_date.strip():
        raise ValueError("Event Date is required.")
    if not event.client_name.strip():
        raise ValueError("Client Name is required.")

    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.cursor()
            if event.id is None:
                # Insert
                cursor.execute(
                    """
                    INSERT INTO events (
                        event_name, event_date, client_name, location, description,
                        income, employee_salary, employee_salary_note,
                        transportation, transportation_note,
                        food, food_note, supplier_payments, supplier_note,
                        utilities_others, utilities_others_note,
                        updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP);
                    """,
                    (
                        event.event_name.strip(),
                        event.event_date.strip(),
                        event.client_name.strip(),
                        event.location.strip(),
                        event.description.strip(),
                        str(parse_currency(event.income)),
                        str(parse_currency(event.employee_salary)),
                        event.employee_salary_note.strip(),
                        str(parse_currency(event.transportation)),
                        event.transportation_note.strip(),
                        str(parse_currency(event.food)),
                        event.food_note.strip(),
                        str(parse_currency(event.supplier_payments)),
                        event.supplier_note.strip(),
                        str(parse_currency(event.utilities_others)),
                        event.utilities_others_note.strip(),
                    ),
                )
                event.id = cursor.lastrowid
            else:
                # Update
                cursor.execute(
                    """
                    UPDATE events SET
                        event_name = ?,
                        event_date = ?,
                        client_name = ?,
                        location = ?,
                        description = ?,
                        income = ?,
                        employee_salary = ?,
                        employee_salary_note = ?,
                        transportation = ?,
                        transportation_note = ?,
                        food = ?,
                        food_note = ?,
                        supplier_payments = ?,
                        supplier_note = ?,
                        utilities_others = ?,
                        utilities_others_note = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?;
                    """,
                    (
                        event.event_name.strip(),
                        event.event_date.strip(),
                        event.client_name.strip(),
                        event.location.strip(),
                        event.description.strip(),
                        str(parse_currency(event.income)),
                        str(parse_currency(event.employee_salary)),
                        event.employee_salary_note.strip(),
                        str(parse_currency(event.transportation)),
                        event.transportation_note.strip(),
                        str(parse_currency(event.food)),
                        event.food_note.strip(),
                        str(parse_currency(event.supplier_payments)),
                        event.supplier_note.strip(),
                        str(parse_currency(event.utilities_others)),
                        event.utilities_others_note.strip(),
                        event.id,
                    ),
                )
            return event
    finally:
        conn.close()


def get_event_by_id(event_id: int, db_path: str = None) -> Optional[Event]:
    """Fetches an event by ID."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE id = ?;", (event_id,))
        row = cursor.fetchone()
        if row:
            return row_to_event(row)
        return None
    finally:
        conn.close()


def delete_event(event_id: int, db_path: str = None) -> bool:
    """Deletes an event by ID."""
    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM events WHERE id = ?;", (event_id,))
            return cursor.rowcount > 0
    finally:
        conn.close()


def get_events_by_month(year: int, month: int, db_path: str = None) -> list[Event]:
    """Fetches all events for a specific year and month, ordered by event_date."""
    month_str = f"{year}-{month:02d}"
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM events 
            WHERE strftime('%Y-%m', event_date) = ?
            ORDER BY event_date ASC, id ASC;
            """,
            (month_str,),
        )
        rows = cursor.fetchall()
        return [row_to_event(r) for r in rows]
    finally:
        conn.close()


def get_all_events(search_query: str = None, db_path: str = None) -> list[Event]:
    """Fetches all events, with optional filter by event_name, client_name, or location."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        if search_query and search_query.strip():
            q = f"%{search_query.strip()}%"
            cursor.execute(
                """
                SELECT * FROM events
                WHERE event_name LIKE ? OR client_name LIKE ? OR location LIKE ?
                ORDER BY event_date DESC, id DESC;
                """,
                (q, q, q),
            )
        else:
            cursor.execute("SELECT * FROM events ORDER BY event_date DESC, id DESC;")
        rows = cursor.fetchall()
        return [row_to_event(r) for r in rows]
    finally:
        conn.close()
