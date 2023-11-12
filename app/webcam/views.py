from django.db.models import F, ExpressionWrapper, FloatField
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter, OrderingFilter

from core.consts import (USER_LATITUDE_FILTER_PARAM_NAME,
                         USER_LONGITUDE_FILTER_PARAM_NAME,
                         USER_MAX_RADIUS_FILTER_PARAM_NAME)
from webcam.filters import WebcamFilter
from webcam.models import Webcam
from webcam.serializers import WebcamSerializer, WebcamLocationFilterSerializer


class WebcamsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class WebcamList(ListAPIView):
    """View for list of webcams"""
    queryset = Webcam.objects.all()
    serializer_class = WebcamSerializer
    pagination_class = WebcamsPagination
    filterset_class = WebcamFilter
    search_fields = (
        'name', 'description', 'category__name', 'country__name', 'country__continent__name', 'user_added__name'
    )
    ordering_fields = ('date_added', 'category__name', 'country__name', 'country__continent__name')
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_queryset(self):
        location_filter_serializer = WebcamLocationFilterSerializer(data=self.request.query_params)
        location_filter_serializer.is_valid(raise_exception=True)

        user_lat = location_filter_serializer.validated_data.get(USER_LATITUDE_FILTER_PARAM_NAME, None)
        user_lon = location_filter_serializer.validated_data.get(USER_LONGITUDE_FILTER_PARAM_NAME, None)
        max_radius = location_filter_serializer.validated_data.get(USER_MAX_RADIUS_FILTER_PARAM_NAME, None)

        if user_lat and user_lon and max_radius:
            return Webcam.objects.annotate(
                distance=ExpressionWrapper(
                    F('latitude') * F('latitude') + F('longitude') * F('longitude'),
                    output_field=FloatField(),
                )).extra(
                    where=["(POW(latitude - %s, 2) + POW(longitude - %s, 2)) <= POW(%s, 2)"],
                    params=[user_lat, user_lon, max_radius]
                )

        return super().get_queryset()
