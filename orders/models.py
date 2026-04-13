from django.db import models
from django.contrib.auth.models import User
from .utils import generate_unique_order_id

# Create your models here.
class OrderStatus(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    order_id = models.CharField(max_length=12, unique=True, blank=True, null=True)
    status = models.ForeignKey(OrderStatus,on_delete=models.SET_NULL,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    objects = OrderManager()
    def get_unique_item_names(self):
        item_names = set()
        for item in self.items.all():
            item_names.add(item.menu_item.name)
        return list(item_names)
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generate_unique_order_id(Order)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'Order #{self.id} - Status: {self.status}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_digits=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    menu_item = models.ForeignKey(Order, on_delete=models.CASCADE)

class OrderManager(models.Manager):
    def get_active_orders(self):
        return self.filter(status__in=['pending', 'processing'])


class Coupon(models.Model):
    code = models.CharField(unique=True)
    discount_percentage = models.DecimalField(max_digits=5,decimal_places=2)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_until = models.DateField()
    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"