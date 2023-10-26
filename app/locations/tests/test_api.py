from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from locations.models import Continent, Country
from locations.serializers import ContinentSerializer, CountrySerializer

CONTINENT_URL = reverse('locations:continents-list')
COUNTRY_URL = reverse('locations:countries-list')


def create_admin(**params):
    return get_user_model().objects.create_superuser(**params)


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class LocationsAPITests(TestCase):
    """Tests the locations API"""
    def setUp(self):
        self.admin_client = APIClient()
        self.user_client = APIClient()

        self.admin = create_admin(
            email='mail@mail.net',
            password='test1234',
        )
        self.user = create_user(
            email='user@mail.net',
            password='test1234',
            name='user',
        )
        self.admin_client.force_authenticate(user=self.admin)
        self.user_client.force_authenticate(user=self.user)

    def test_create_continent_by_admin_success(self):
        """Test creating continent by admin is successful"""
        payload = {
            'name': 'Europa',
        }

        res = self.admin_client.post(CONTINENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, msg='Response status is incorrect')

        continent = Continent.objects.get(name=payload['name'])
        self.assertEqual(continent.name, payload['name'])

    def test_create_continent_by_user_failed(self):
        """Test creating continent by user is failed"""
        payload = {
            'name': 'Europa',
        }

        res = self.user_client.post(CONTINENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN, msg='Response status is incorrect')

    def test_create_country_by_admin_successful(self):
        """Test creating country by admin is successful"""
        continent = Continent.objects.create(
            name='Europa',
        )

        payload = {
            'name': 'Polska',
            'continent': continent.id,
        }

        res = self.admin_client.post(COUNTRY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, msg='Response status is incorrect')

        country = Country.objects.get(name=payload['name'])
        self.assertEqual(country.name, payload['name'], msg='Country name is incorrect')

        self.assertEqual(country.continent.name, continent.name, msg='Continent of the created country is incorrect')

    def test_create_country_by_user_failed(self):
        """Test creating country by user is failed"""
        continent = Continent.objects.create(
            name='Europa',
        )

        payload = {
            'name': 'Polska',
            'continent': continent.id,
        }

        res = self.user_client.post(COUNTRY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN, msg='Response status is incorrect')

    def test_list_continents_by_admin_successful(self):
        """Test listing continents by admin is successful"""
        _ = Continent.objects.create(name='Europa')
        _ = Continent.objects.create(name='Azja')

        res = self.admin_client.get(CONTINENT_URL)

        continents = Continent.objects.all().order_by('id')
        serializer = ContinentSerializer(continents, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_single_continent_by_admin_successful(self):
        """Test getting single continent by admin is successful"""
        europa = Continent.objects.create(name='Europa')

        url = reverse('locations:continents-detail', args=[europa.id])
        res = self.admin_client.get(url)

        serializer = ContinentSerializer(europa)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_total_update_continent_by_admin_successful(self):
        """Test fully updating single continent by admin is successful"""
        europe = Continent.objects.create(name='Europa')

        payload = {
            'name': 'Europe',
        }

        url = reverse('locations:continents-detail', args=[europe.id])
        res = self.admin_client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], payload['name'])

    def test_remove_continent_by_admin_successful(self):
        """Test remove single continent by admin is successful"""
        europe = Continent.objects.create(name='Europa')
        url = reverse('locations:continents-detail', args=[europe.id])

        _ = self.admin_client.delete(url)
        get_res = self.admin_client.get(url)

        self.assertEqual(get_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_countries_by_admin_successful(self):
        """Test listing countries by admin is successful"""
        europe = Continent.objects.create(name='Europa')

        _ = Country.objects.create(name='Polska', continent=europe)
        _ = Country.objects.create(name='Grecja', continent=europe)

        res = self.admin_client.get(COUNTRY_URL)

        countries = Country.objects.all().order_by('id')
        serializer = CountrySerializer(countries, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_single_country_by_admin_successful(self):
        """Test getting single country by admin is successful"""
        europe = Continent.objects.create(name='Europa')
        poland = Country.objects.create(
            name='Polska',
            continent=europe,
        )

        url = reverse('locations:countries-detail', args=[poland.id])
        res = self.admin_client.get(url)

        serializer = CountrySerializer(poland)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_total_update_country_by_admin_successful(self):
        """Test fully updating single country by admin is successful"""
        europe = Continent.objects.create(name='Europa')
        poland = Country.objects.create(name='Polska')

        new_continent = Continent.objects.create(name='Azja')

        payload = {
            'name': 'Armenia',
            'continent': new_continent.id,
        }

        url = reverse('locations:countries-detail', args=[poland.id])
        res = self.admin_client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], payload['name'])
        self.assertEqual(res.data['continent'], payload['continent'])
