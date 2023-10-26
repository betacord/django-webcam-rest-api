from django.test import TestCase

from locations import models


class UserModelTests(TestCase):
    """Tests for User model"""

    def test_successful_create_continent(self):
        """Test creating a new continent is successful"""

        continent_name = 'Europa'
        continent = models.Continent.objects.create(name=continent_name)

        self.assertEqual(continent.name, continent_name, msg='Continent name is incorrect')

    def test_successful_create_country(self):
        """Test creating a new country is successful"""

        continent_name = 'Europa'
        continent = models.Continent.objects.create(name=continent_name)

        country_name = 'Polska'
        country = models.Country.objects.create(
            name=country_name,
            continent=continent,
        )

        self.assertEqual(country.name, country_name, msg='Country name is incorrect')
        self.assertEqual(country.continent.name, continent_name, msg='Continent name of created country is incorrect')
