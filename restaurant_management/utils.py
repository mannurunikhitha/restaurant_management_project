from datetime import datetime

def format_datetime(dt: datetime | None) -> str:
    if not dt:
        return "" # or "N/A"
    return dt.strftime("%B %d, %Y at %I:%M %P")
    