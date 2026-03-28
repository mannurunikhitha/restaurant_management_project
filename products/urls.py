from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = router.urls

urlpatterns = [
    path('items/', ItemView.as_view(), name='item-list'),
]