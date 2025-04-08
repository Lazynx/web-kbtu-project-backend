from rest_framework import serializers
from .models import Booking
from tours.serializers import TourSerializer
from django.contrib.auth.models import User

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    tour = TourSerializer()

    class Meta:
        model = Booking
        fields = ['id', 'user', 'tour', 'booking_date']