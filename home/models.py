from django.db import models
from datetime import date
from django.db.models import Count
# Create your models here.

class Table(models.Model):
    table_number = models.IntegerField()
    capacity = models.IntegerField()
    is_available = models.BooleanField(default= True, null=True, blank=True)

    def __str__(self):
        return str(self.table_number)

class MenuCategory(models.Model):
    name=models.CharField(max_length=100,unique=True)
    category_name = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.name

class MenuItemManager(models.Manager):
    def get_top_selling_items(self, num_items=5):
        return self.annotate(
            total_orders = Count('orderitem_set')
            
        ).order_by('-total_orders')[:num_items]

class Restaurant(models.Model):
    name=models.CharField(max_length=255)
    address=models.TextField()
    has_delivery=models.BooleanField(default=False)
    def __str__(self):
        return self.name

class DailyOperatingHours(models.Model):
    day = models.CharField(max_length=10)
    open_time = models.TimeField()
    close_time = models.TimeField()
    def __str__(self):
        return f"{self.day}: {self.open_time} - {self.close_time}"

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    ingredients = models.ManyToManyField('Ingredient', related_name="menu_items")
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class DailySpecialManager(models.Manager):
    def upcoming(self):
        today = date.today()
        return self.filter(date__gte=today)

class DailySpecial(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = DailySpecialManager()
    @staticmethod 
    def get_random_special():
        specials = DailySpecial.objects.all()
        if specials.exists():
            return specials.order_by('?').first()
        return None

class NutritionalInformation(models.Model):
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE, related_name='nutrition')
    calories = models.IntegerField()
    protein_grams = models.DecimalField(max_digits=5, decimal_places=2)
    fat_grams = models.DecimalField(max_digits=5, decimal_places=2)
    carbohydrate_grams = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return f"{self.menu_item.name} - {self.calories} kcal"

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

