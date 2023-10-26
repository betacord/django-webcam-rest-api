from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from locations.models import Continent, Country
from locations.serializers import ContinentSerializer, CountrySerializer


class ContinentViewSet(viewsets.ModelViewSet):
    """CRUD for continent. Only for admin user"""
    serializer_class = ContinentSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminUser, )
    queryset = Continent.objects.all()


class CountryViewSet(viewsets.ModelViewSet):
    """CRUD for country. Only for admin user"""
    serializer_class = CountrySerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminUser, )
    queryset = Country.objects.all()
