import string
import secrets
from .models import Coupon
from django.db.models import Sum
from .models import Order

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