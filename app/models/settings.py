from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Settings:
    id: int = 1
    business_name: str = "Chirathma Flora"
    pin_hash: Optional[str] = None
    pin_salt: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @property
    def has_pin(self) -> bool:
        return bool(self.pin_hash and self.pin_salt)
