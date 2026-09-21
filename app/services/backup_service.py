import os
import shutil
import sqlite3
from app.database.connection import get_db_path, get_connection


def create_backup(dest_path: str, db_path: str = None) -> str:
    """
    Creates a snapshot backup of the SQLite database.
    Uses sqlite3 backup API for safety.
    """
    source_path = get_db_path(db_path)
    if not os.path.exists(source_path):
        raise FileNotFoundError("Source database file does not exist.")

    src_conn = sqlite3.connect(source_path)
    dest_conn = sqlite3.connect(dest_path)
    try:
        with dest_conn:
            src_conn.backup(dest_conn)
        return dest_path
    finally:
        src_conn.close()
        dest_conn.close()


def validate_backup_file(file_path: str) -> bool:
    """
    Validates whether a given file is a valid Chirathma Flora SQLite database backup.
    Checks for required tables: settings, events, monthly_expenses.
    """
    if not os.path.exists(file_path):
        return False

    try:
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = {row[0] for row in cursor.fetchall()}
        conn.close()

        required = {"settings", "events", "monthly_expenses"}
        return required.issubset(tables)
    except Exception:
        return False


def restore_backup(backup_path: str, db_path: str = None) -> None:
    """
    Restores database from a valid backup file.
    Validates backup file prior to overwriting target database.
    """
    if not validate_backup_file(backup_path):
        raise ValueError("Invalid Backup: The selected file could not be restored.")

    target_path = get_db_path(db_path)

    # Use SQLite backup API to safely restore into current database
    src_conn = sqlite3.connect(backup_path)
    target_conn = sqlite3.connect(target_path)
    try:
        with target_conn:
            src_conn.backup(target_conn)
    finally:
        src_conn.close()
        target_conn.close()
