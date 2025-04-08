from django.urls import path
from .views import CreateBookingView

urlpatterns = [
    path('bookings/', CreateBookingView.as_view(), name='create_booking'),
]
