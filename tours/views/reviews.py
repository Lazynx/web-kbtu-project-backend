from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers import ReviewSerializer

from django.shortcuts import get_object_or_404
from ..models import Review

@extend_schema(
    request=ReviewSerializer,
    responses={
        201: ReviewSerializer,
        400: OpenApiResponse(description='Неверные данные'),
    },
    description='Создать отзыв о туре',
    tags=['Reviews'],
)

@extend_schema(
    methods=['DELETE'],
    description='Удалить отзыв (только админ)',
    tags=['Reviews'],
    responses={
        204: OpenApiResponse(description='Успешно удалено'),
        403: OpenApiResponse(description='Запрещено'),
        404: OpenApiResponse(description='Не найдено'),
    }
)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_review(request, review_id): 
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
