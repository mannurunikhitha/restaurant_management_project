from django.contrib import admin
from .models import *
# Register your models here.
def mark_orders_processed(modeladmin, request, queryset):
    queryset.update(status='Processed')

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status']
    actions = [mark_orders_processed]

admin.site.register(Order, OrderAdmin)
admin.site.register(PaymentMethod)