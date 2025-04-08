from django.urls import path
from .views import get_tours

urlpatterns = [
    path('tours/', get_tours, name='get_tours'),
]