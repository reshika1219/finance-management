from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

TWO_PLACES = Decimal("0.01")


def parse_currency(val) -> Decimal:
    """
    Parses string or numeric input safely to Decimal with 2 decimal places.
    Empty string, None, or invalid strings default to Decimal('0.00').
    Negative values are allowed for calculations, but manually typed negative entries
    can be validated at form level.
    """
    if val is None:
        return Decimal("0.00")

    if isinstance(val, (int, float)):
        val = str(val)

    if isinstance(val, str):
        cleaned = val.strip().replace("Rs.", "").replace("Rs", "").replace(",", "").strip()
        if not cleaned:
            return Decimal("0.00")
        try:
            d = Decimal(cleaned)
            return d.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
        except InvalidOperation:
            raise ValueError(f"Invalid currency amount: '{val}'")

    if isinstance(val, Decimal):
        return val.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

    return Decimal("0.00")


def format_currency(val: Decimal | str | float | int, include_prefix: bool = True) -> str:
    """
    Formats a decimal or numeric value as Sri Lankan Rupees:
    Example: Rs. 1,250,000.00 or -Rs. 50,000.00
    """
    if not isinstance(val, Decimal):
        try:
            val = parse_currency(val)
        except ValueError:
            val = Decimal("0.00")
    else:
        val = val.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

    is_negative = val < 0
    abs_val = abs(val)

    formatted_num = f"{abs_val:,.2f}"

    if include_prefix:
        if is_negative:
            return f"-Rs. {formatted_num}"
        return f"Rs. {formatted_num}"
    else:
        if is_negative:
            return f"-{formatted_num}"
        return formatted_num
