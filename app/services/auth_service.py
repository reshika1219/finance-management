from app.services.settings_service import get_settings, update_pin
from app.utils.security import hash_pin, verify_pin, is_valid_pin_format


class AuthService:
    def __init__(self, db_path: str = None):
        self.db_path = db_path

    def is_first_launch(self) -> bool:
        """Returns True if no PIN has been set up yet."""
        settings = get_settings(self.db_path)
        return not settings.has_pin

    def setup_pin(self, pin: str, confirm_pin: str) -> None:
        """Sets up the initial 4-digit PIN."""
        if not is_valid_pin_format(pin):
            raise ValueError("PIN must be exactly 4 numeric digits.")

        if pin != confirm_pin:
            raise ValueError("PINs do not match. Please try again.")

        pin_hash, pin_salt = hash_pin(pin)
        update_pin(pin_hash, pin_salt, self.db_path)

    def verify(self, pin: str) -> bool:
        """Verifies the entered PIN against saved database hash."""
        settings = get_settings(self.db_path)
        if not settings.has_pin:
            return False
        return verify_pin(pin, settings.pin_hash, settings.pin_salt)

    def change_pin(self, current_pin: str, new_pin: str, confirm_new_pin: str) -> None:
        """Changes existing PIN after verifying current PIN."""
        if not self.verify(current_pin):
            raise ValueError("Current PIN is incorrect.")

        if not is_valid_pin_format(new_pin):
            raise ValueError("New PIN must be exactly 4 numeric digits.")

        if new_pin != confirm_new_pin:
            raise ValueError("New PINs do not match. Please try again.")

        new_hash, new_salt = hash_pin(new_pin)
        update_pin(new_hash, new_salt, self.db_path)
