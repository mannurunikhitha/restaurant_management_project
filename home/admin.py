from django.contrib import admin
from .models import Restaurant
from .models import DailyOperatingHours
from.models import MenuCategory

# Register your models here.
admin.site.register(Restaurant)

admin.site.register(DailyOperatingHours)

admin.site.register(MenuCategory)