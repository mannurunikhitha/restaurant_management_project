from datetime import datetime, time
from .models import DailyOperatingHours

def get_today_operating_hours():
    today = datetime.now().strftime('%A')

    try:
        hours = DailyOperatingHours.objects.get(day=today)
        return (hours.open_time, hours.close_time)
    except DailyOperatingHours.DoesNotExist:
        return (None, None)

def is_restaurant_open():
    now = datetime.now()
    current_day = now.weekday()
    current_time = now.time()
    if current_day < 5:
        open_time = time(9, 0)
        close_time = time(22, 0)
    else:
        open_time = time(10, 0)
        close_time = time(23, 0)
    if open_time <= current_time <= close_time:
        return True
    return False