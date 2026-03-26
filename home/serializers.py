from rest_framework import serializers
from .models import MenuCategory, MenuItem

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ["name"]

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'