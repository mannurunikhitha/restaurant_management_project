from django.db import models
# Create your models here.
class MenuCategory(models.Model):
    name=models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name=models.CharField(max_length=255)
    address=models.TextField()
    has_delivery=models.BooleanField(default=False)
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_length=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name