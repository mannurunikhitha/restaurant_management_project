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

class DailySpecial(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    @staticmethod 
    def get_random_special():
        specials = DailySpecial.objects.all()
        if specials.exists():
            return specials.order_by('?').first()
        return None