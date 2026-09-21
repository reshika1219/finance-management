from app.database.connection import get_connection
from app.models.settings import Settings


def get_settings(db_path: str = None) -> Settings:
    """Retrieves the application settings."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, business_name, pin_hash, pin_salt, created_at, updated_at FROM settings WHERE id = 1;")
        row = cursor.fetchone()
        if row:
            return Settings(
                id=row["id"],
                business_name=row["business_name"],
                pin_hash=row["pin_hash"],
                pin_salt=row["pin_salt"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )
        return Settings()
    finally:
        conn.close()


def update_business_name(name: str, db_path: str = None) -> None:
    """Updates the business name in settings."""
    clean_name = name.strip()
    if not clean_name:
        raise ValueError("Business name cannot be empty.")

    conn = get_connection(db_path)
    try:
        with conn:
            conn.execute(
                "UPDATE settings SET business_name = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1;",
                (clean_name,)
            )
    finally:
        conn.close()


def update_pin(pin_hash: str, pin_salt: str, db_path: str = None) -> None:
    """Updates the PIN hash and salt in settings."""
    conn = get_connection(db_path)
    try:
        with conn:
            conn.execute(
                "UPDATE settings SET pin_hash = ?, pin_salt = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1;",
                (pin_hash, pin_salt)
            )
    finally:
        conn.close()
