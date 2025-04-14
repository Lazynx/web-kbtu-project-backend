from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Booking
from ..serializers import BookingSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.shortcuts import get_object_or_404
import uuid

class CreateBookingView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=BookingSerializer,
        responses={
            201: BookingSerializer,
            400: OpenApiResponse(description="Неверные данные"),
            401: OpenApiResponse(description="Не авторизован"),
        },
        description="Создать бронирование для текущего пользователя",
        tags=["Bookings"],
    )
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: BookingSerializer(many=True)},
        description="Получить список бронирований текущего пользователя",
        tags=["Bookings"],
    )
    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=BookingSerializer,
        responses={
            201: BookingSerializer,
            400: OpenApiResponse(description="Неверные данные"),
        },
        description="Создать новое бронирование",
        tags=["Bookings"],
    )
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: BookingSerializer,
            404: OpenApiResponse(description="Бронирование не найдено"),
        },
        description="Получить детали бронирования",
        tags=["Bookings"],
    )
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    @extend_schema(
        request=BookingSerializer,
        responses={
            200: BookingSerializer,
            400: OpenApiResponse(description="Неверные данные"),
            404: OpenApiResponse(description="Бронирование не найдено"),
        },
        description="Обновить бронирование",
        tags=["Bookings"],
    )
    def put(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            204: OpenApiResponse(description="Бронирование удалено"),
            404: OpenApiResponse(description="Бронирование не найдено"),
        },
        description="Удалить бронирование",
        tags=["Bookings"],
    )
    def delete(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)