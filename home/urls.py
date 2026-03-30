from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'menu-items', MenuItemViewSet)

urlpatterns = [
    path("categories/",MenuCategoryListView.as_view(),name="menu-categories"),
    path("today-hours/",show_today_hours),
    path('featured-menu/', FeaturedMenuItemListView.as_view(), name='featured-menu'),
    path('api/menu-items/<int:pk>/ingredients/', MenuCategoryListView.as_view(), name='menu-item-ingredients'),
    path('api/',include(router.urls)),
]