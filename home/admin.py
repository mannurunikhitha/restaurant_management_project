from django.contrib import admin
from .models import Restaurant
from .models import DailyOperatingHours
from.models import MenuCategory

# Register your models here.

admin.site.register(DailyOperatingHours)

admin.site.register(MenuCategory)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone_number', 'email', 'is_active']
    search_fields = ['name', 'address']
    list_filter = ['is_active']
    ordering = ['name']
    list_per_page = 10
    list_display_links = ['name']
    list_editable = ['is_active']
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'address')
        }),
        ('Contact Info', {
            'fields': ('phone_number', 'email')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )