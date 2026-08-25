from datetime import timezone
from zoneinfo import ZoneInfo


INDIA_TIMEZONE = ZoneInfo("Asia/Kolkata")


def to_ist(value):

    if not value:
        return None

    utc_value = value.replace(tzinfo=timezone.utc)

    return utc_value.astimezone(INDIA_TIMEZONE)


def format_ist_datetime(value):
    """
    Convert a database UTC datetime to IST
    and return it in a user-friendly format.
    """

    ist_value = to_ist(value)

    if not ist_value:
        return ""

    return ist_value.strftime(
        "%d %b %Y, %I:%M %p"
    )