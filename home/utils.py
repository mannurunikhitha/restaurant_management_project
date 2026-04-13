from datetime import datetime, time
from .models import DailyOperatingHours
import re
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def send_email(to_email, subject, message):
    """
    Reusable function to send emails
    Args:
        to_email (str): Recipient email
        subject (str): Email subject
        message (str): Email body

    Returns:
        dict: status and message
    """
    try:
        validate_email(to_email)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False
        )
        return {"status": "success", "message": "Email sent successfullt"}
    except ValidationError:
        return {"status": "error", "message": "Invalid email address"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

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

def is_valid_phone_number(phone):
    pattern = r'^(\+?\d{1,3})?[\s-]?\d{10}$'
    if re.match(pattern, phone):
        return True
    return False