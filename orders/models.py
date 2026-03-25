from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class OrderStatus(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.name

class Order(models.Model):
    status = models.ForeignKey(OrderStatus,on_delete=models.SET_NULL,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f'Order #{self.id} - Status: {self.status}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)


class Coupon(models.Model):
    code = models.CharField(unique=True)
    discount_percentage = models.DecimalField(max_digits=5,decimal_places=2)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_until = models.DateField()
    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"