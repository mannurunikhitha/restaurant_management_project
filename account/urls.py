from django.urls import path
from .views import *

urlpatterns = [
    path("profile/update", UserProfileViewSet.as_view({"put": "update"})),
]