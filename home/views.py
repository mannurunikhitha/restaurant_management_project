from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import MenuCategory, MenuItem
from .serializers import MenuCategorySerializer
from .utils import get_today_operating_hours
from django.http import HttpResponse
from .serializers import MenuItemSerializer

# Create your views here.
class MenuCategoryListView(ListAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

def show_today_hours(request):
    open_time, close_time = get_today_operating_hours()

    if open_time and close_time:
        return HttpResponse(f"Today open from {open_time} - {close_time}")
    else:
        return HttpResponse('Restaurant is closed today')

class FeaturedMenuItemListView(ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return MenuItem.objects.filter(is_featured=True)