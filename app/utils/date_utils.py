from datetime import datetime, date
import calendar

DISPLAY_DATE_FORMAT = "%d/%m/%Y"
ISO_DATE_FORMAT = "%Y-%m-%d"

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


def format_display_date(date_obj: date | str) -> str:
    """Converts a date object or ISO string to DD/MM/YYYY format."""
    if isinstance(date_obj, str):
        date_obj = parse_iso_date(date_obj)
    return date_obj.strftime(DISPLAY_DATE_FORMAT)


def parse_display_date(date_str: str) -> date:
    """Parses DD/MM/YYYY string into a datetime.date object."""
    dt = datetime.strptime(date_str.strip(), DISPLAY_DATE_FORMAT)
    return dt.date()


def format_iso_date(date_obj: date | str) -> str:
    """Converts a date object or DD/MM/YYYY string to YYYY-MM-DD format."""
    if isinstance(date_obj, str):
        if "/" in date_obj:
            date_obj = parse_display_date(date_obj)
        else:
            return date_obj
    return date_obj.strftime(ISO_DATE_FORMAT)


def parse_iso_date(iso_str: str) -> date:
    """Parses YYYY-MM-DD string into a datetime.date object."""
    dt = datetime.strptime(iso_str.strip(), ISO_DATE_FORMAT)
    return dt.date()


def get_month_year_display(year: int, month: int) -> str:
    """Returns formatted month string like 'September 2026'."""
    return f"{MONTH_NAMES[month - 1]} {year}"


def parse_month_name(month_name: str) -> int:
    """Returns 1-12 index for a month name string."""
    name_clean = month_name.strip().capitalize()
    if name_clean in MONTH_NAMES:
        return MONTH_NAMES.index(name_clean) + 1
    raise ValueError(f"Invalid month name: '{month_name}'")


def get_previous_month(year: int, month: int) -> tuple[int, int]:
    """Returns (prev_year, prev_month)."""
    if month == 1:
        return year - 1, 12
    return year, month - 1


def get_next_month(year: int, month: int) -> tuple[int, int]:
    """Returns (next_year, next_month)."""
    if month == 12:
        return year + 1, 1
    return year, month + 1


def get_month_range_tuples(start_year: int, start_month: int, end_year: int, end_month: int) -> list[tuple[int, int]]:
    """Generates a list of (year, month) tuples from start to end inclusive."""
    result = []
    curr_y, curr_m = start_year, start_month
    while (curr_y < end_year) or (curr_y == end_year and curr_m <= end_month):
        result.append((curr_y, curr_m))
        curr_y, curr_m = get_next_month(curr_y, curr_m)
    return result
