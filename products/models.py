from django.db import models

# Create your models here.
class Item(models.Model):
    item_name = models.CharField(max_length=150)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.item_name)

class Category(models.Model):
    category_name = models.CharField(max_length=100)



class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    operating_days = models.CharField(
        max_length=100,
        help_text="Example: Mon,Tue,Wed,Thu,Fri"
    )
    def __str__(self):
        return self.name