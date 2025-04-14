from django.urls import path
from .views import (
    tour_list_create,
    create_review,
    TourDetailView,
    BookingListCreateView,
    BookingDetailView,
    create_category,
)

urlpatterns = [
    path("tours/", tour_list_create, name="tour_list_create"),
    path("tours/<uuid:tour_id>/", TourDetailView.as_view(), name="tour_detail"),
    path("categories/", create_category, name="create_category"),
    path("bookings/", BookingListCreateView.as_view(), name="booking_list_create"),
    path("bookings/<uuid:booking_id>/", BookingDetailView.as_view(), name="booking_detail"),
    path("reviews/", create_review, name="create_review"),
]