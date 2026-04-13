import string
import secrets
from django.db.models import Model
from .models import Coupon
from django.db.models import Sum
from .models import Order
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

def send_order_confirmation_email(order_id, customer_email, customer_name=None, items=None, total_amount=None):
    try:
        try:
            validate_email(customer_email)
        except ValidationError:
            return {"status": "error", "message": "Invalid email"}
        subject = f"Order Confirmation - #{order_id}"
        items_text = "\n".join([f"- {item}" for item in items]) if items else "N/A"
        message = f"""
Hi {customer_name or "Customer"},

Your order has been placed successfully! 🎉

Order ID: {order_id}

Items:
{items_text}

Total Amount: {total_amount if total_amount else 'N/A'}

We'll nofity you once your order is ready.

Thank you for ordering with us! 😊"""

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email],
            fail_silently=False,
        )
        return {"status": "success", "message": "Email sent"}
    except Exception as e:
        logger.error(f"Order Email Error (Order {order_id}): {str(e)}")
        return {"status": "error", "message": "Email failed"}

def generate_coupon_code(length=10):
    characters = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(secrets.choice(characters) for _ in range(length))

        if not Coupon.objects.filter(code=code).exists():
            return code

def get_daily_sales_total(date):
    orders = Order.objects.filter(created_at__date=date)
    total = orders.aggregate(total_sum=Sum('total_price'))['total_sum']
    return total if total is not None else 0

def calculate_tip_amount(order_total, tip_percentage):
    order_total = Decimal(order_total)
    tip_percentage = Decimal(tip_percentage)
    tip_amount = order_total * (tip_percentage/Decimal('100'))
    tip_amount = tip_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return tip_amount

def generate_unique_order_id(model: Model, field_name: str = "order_id", length: int = 8) -> str:
    """
    Generates a unique short alphanumeric ID for a given model field.

    Args:
        model: Django model class where the ID will be stored (e.g., Order)
        field_name: The field to check uniqueness against (defaukt: 'order_id')
        length: Length of the generated ID (default: 8)
    Returns:
        A unique aplhanumeric string
    """
    characters = string.ascii_uppercase + string.digits
    while True:
        random_id = ''.join(secrets.choice(characters) for _ in range(length))
        if not model.objects.filter(**{field_name: random_id}).exists():
            return random_id