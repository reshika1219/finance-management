import sqlite3
from app.database.connection import get_connection

CREATE_SETTINGS_TABLE = """
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    business_name TEXT NOT NULL DEFAULT 'Chirathma Flora',
    pin_hash TEXT,
    pin_salt TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    event_date TEXT NOT NULL,
    client_name TEXT NOT NULL,
    location TEXT DEFAULT '',
    description TEXT DEFAULT '',
    income TEXT NOT NULL DEFAULT '0.00',
    employee_salary TEXT DEFAULT '0.00',
    employee_salary_note TEXT DEFAULT '',
    transportation TEXT DEFAULT '0.00',
    transportation_note TEXT DEFAULT '',
    food TEXT DEFAULT '0.00',
    food_note TEXT DEFAULT '',
    supplier_payments TEXT DEFAULT '0.00',
    supplier_note TEXT DEFAULT '',
    utilities_others TEXT DEFAULT '0.00',
    utilities_others_note TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_MONTHLY_EXPENSES_TABLE = """
CREATE TABLE IF NOT EXISTS monthly_expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    rent TEXT DEFAULT '0.00',
    electricity TEXT DEFAULT '0.00',
    water TEXT DEFAULT '0.00',
    telephone TEXT DEFAULT '0.00',
    others TEXT DEFAULT '0.00',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(year, month)
);
"""


def init_db(db_path: str = None) -> None:
    """Initializes SQLite database tables and default settings row if missing."""
    conn = get_connection(db_path)
    try:
        with conn:
            conn.execute(CREATE_SETTINGS_TABLE)
            conn.execute(CREATE_EVENTS_TABLE)
            conn.execute(CREATE_MONTHLY_EXPENSES_TABLE)

            # Insert initial settings row if table is empty
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM settings WHERE id = 1;")
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.execute(
                    "INSERT INTO settings (id, business_name) VALUES (1, 'Chirathma Flora');"
                )
    finally:
        conn.close()
