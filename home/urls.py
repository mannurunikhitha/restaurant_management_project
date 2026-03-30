from django.urls import path
from .views import *

urlpatterns = [
    path("categories/",MenuCategoryListView.as_view(),name="menu-categories"),
    path("today-hours/",show_today_hours),
    path('featured-menu/', FeaturedMenuItemListView.as_view(), name='featured-menu'),
    path('api/menu-items/<int:pk>/ingredients/', MenuCategoryListView.as_view(), name='menu-item-ingredients'),
]