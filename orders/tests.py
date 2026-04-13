from django.test import TestCase
from decimal import Decimal
from orders.models import Order, OrderItem
from home.models import MenuItem

# Create your tests here.

class OrderModelTest(TestCase):
    def test_calculate_total(self):
        order = Order.objects.create(order_id='TEST001')
        item1 = MenuItem.objects.create(name="Pizza", price=200)
        item2 = MenuItem.objects.create(name="Burger", price=100)

        OrderItem.objects.create(order=order, menu_item=item1, quantity=2, price=200)
        OrderItem.objects.create(order=order, menu_item=item2, quantity=1, price=100)

        total = order.calculate_total()

        self.assertEqual(total, Decimal('500.00'))
