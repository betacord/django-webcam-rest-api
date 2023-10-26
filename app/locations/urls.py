from django.urls import path
from rest_framework.routers import SimpleRouter

from locations import views

app_name = 'locations'

router = SimpleRouter()

router.register('continents', views.ContinentViewSet, basename='continents')
router.register('countries', views.CountryViewSet, basename='countries')

urlpatterns = router.urls
