import os
import tempfile
from decimal import Decimal
import pytest

from app.database.schema import init_db
from app.models.event import Event
from app.services.event_service import save_event, get_all_events
from app.services.backup_service import create_backup, restore_backup, validate_backup_file


def test_backup_and_restore():
    db1_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db1_path = db1_file.name
    db1_file.close()

    db2_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db2_path = db2_file.name
    db2_file.close()

    backup_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    backup_path = backup_file.name
    backup_file.close()

    try:
        init_db(db1_path)
        init_db(db2_path)

        # Populate db1
        save_event(Event(
            event_name="Event Original", event_date="2026-09-01", client_name="Client A",
            income=Decimal("100000.00")
        ), db1_path)

        assert len(get_all_events(db_path=db1_path)) == 1

        # Backup db1
        create_backup(backup_path, db1_path)
        assert validate_backup_file(backup_path) is True

        # Restore into db2
        restore_backup(backup_path, db2_path)
        events_db2 = get_all_events(db_path=db2_path)
        assert len(events_db2) == 1
        assert events_db2[0].event_name == "Event Original"
    finally:
        for p in (db1_path, db2_path, backup_path):
            if os.path.exists(p):
                os.remove(p)
