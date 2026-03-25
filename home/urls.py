from django.urls import path
from .views import *

urlpatterns = [
    path("categories/",MenuCategoryListView.as_view(),name="menu-categories"),
    path("today-hours/",show_today_hours),
]