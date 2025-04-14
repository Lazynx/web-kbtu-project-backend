from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Tour
from ..serializers import TourSerializer, TourFilterSerializer, CategorySerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.shortcuts import get_object_or_404

@extend_schema(
    methods=["GET"],
    responses={200: TourSerializer(many=True)},
    description="Получить список активных туров",
    parameters=[TourFilterSerializer],
    tags=["Tours"],
)
@extend_schema(
    methods=["POST"],
    request=TourSerializer,
    responses={
        201: TourSerializer,
        400: OpenApiResponse(description="Неверные данные"),
        401: OpenApiResponse(description="Не авторизован"),
    },
    description="Создать новый тур",
    tags=["Tours"],
)
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def tour_list_create(request):
    if request.method == "GET":
        tours = Tour.objects.active().prefetch_related("reviews")
        serializer = TourFilterSerializer(data=request.query_params)
        if serializer.is_valid():
            if serializer.validated_data.get("category_id"):
                tours = tours.filter(category_id=serializer.validated_data["category_id"])
            if serializer.validated_data.get("min_price"):
                tours = tours.filter(price__gte=serializer.validated_data["min_price"])
            if serializer.validated_data.get("max_price"):
                tours = tours.filter(price__lte=serializer.validated_data["max_price"])
            if serializer.validated_data.get("start_date"):
                tours = tours.filter(start_date__gte=serializer.validated_data["start_date"])
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(TourSerializer(tours, many=True).data)

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = TourSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=CategorySerializer,
    responses={
        201: CategorySerializer,
        400: OpenApiResponse(description="Неверные данные"),
        401: OpenApiResponse(description="Не авторизован"),
    },
    description="Создать новую категорию",
    tags=["Categories"],
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TourDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            200: TourSerializer,
            404: OpenApiResponse(description="Тур не найден"),
        },
        description="Получить детали конкретного тура",
        tags=["Tours"],
    )
    def get(self, request, tour_id):
        tour = get_object_or_404(Tour, id=tour_id, is_active=True)
        serializer = TourSerializer(tour)
        return Response(serializer.data)