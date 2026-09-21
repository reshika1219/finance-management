import os
import sqlite3
from pathlib import Path

DEFAULT_DB_NAME = "chirathma_flora.db"


def get_db_path(custom_path: str = None) -> str:
    """Returns absolute path to SQLite database file."""
    if custom_path:
        return custom_path

    # Standard location in user's home AppData or local directory
    if os.name == "nt":
        app_data = os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))
        db_dir = Path(app_data) / "ChirathmaFlora"
    else:
        db_dir = Path.home() / ".chirathma_flora"

    db_dir.mkdir(parents=True, exist_ok=True)
    return str(db_dir / DEFAULT_DB_NAME)


def get_connection(db_path: str = None) -> sqlite3.Connection:
    """Creates and returns a sqlite3 connection with Row factory enabled."""
    path = get_db_path(db_path)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
