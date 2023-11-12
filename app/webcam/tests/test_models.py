from datetime import date

from django.test import TestCase

from locations.models import Country, Continent
from user.models import User
from webcam import models
from webcam.helpers import Location


class CategoryModelTests(TestCase):
    """Tests for webcam category model"""
    def test_successful_create_category(self):
        """Test creating a new category is successful"""
        category_name = 'Jeziora'
        category = models.Category.objects.create(name=category_name)

        self.assertEqual(category.name, category_name, msg='Category name is incorrect')


class WebcamModelTests(TestCase):
    """Tests for webcam model"""
    def setUp(self):
        self.country_name = 'Polska'
        self.continent = Continent.objects.create(name='Europa')
        self.country = Country.objects.create(name=self.country_name, continent=self.continent)
        self.user = User.objects.create(
            email='janusz@polska.net',
            name='Janusz',
            is_active=True,
            is_staff=False,
        )

    def test_successful_create_webcam(self):
        """Test creating a new webcam is successful"""
        name = 'Jezioro Kisajno, Stanica Stranda'
        category_name = 'Jeziora'
        category = models.Category.objects.create(name=category_name)
        location = Location(longitude=0.01, latitude=0.02)
        description = 'Test desc'
        url = 'https://mazury24.eu/mazury-kamery-live/jezioro-kisajno-stanica-wodna-stranda,472'
        thumbnail = 'https://mazury24.eu/img/kamery/m_stranda.webp'
        date_added = date.today()
        user_added = self.user

        webcam = models.Webcam.objects.create(
            name=name,
            description=description,
            url=url,
            thumbnail_url=thumbnail,
            latitude=location.latitude,
            longitude=location.longitude,
            category=category,
            country=self.country,
            user_added=user_added,
        )

        self.assertEqual(webcam.name, name, msg='Webcam name is incorrect')
        self.assertEqual(webcam.description, description, msg='Webcam description is incorrect')
        self.assertEqual(webcam.url, url, msg='Webcam url is incorrect')
        self.assertEqual(webcam.thumbnail_url, thumbnail, msg='Webcam thumbnail_url is incorrect')
        self.assertEqual(location, Location(webcam.latitude, webcam.longitude), msg='Webcam location is incorrect')
        self.assertEqual(webcam.category.name, category_name, msg='Webcam category is incorrect')
        self.assertEqual(webcam.country.name, self.country_name, msg='Webcam country is incorrect')
        self.assertLessEqual((webcam.date_added - date_added).days, 1, msg='Date of creating webcam is incorrect')
        self.assertEqual(webcam.user_added, user_added, msg='User adding webcam is incorrect')

    def test_comments_referenced_successfully_to_webcam(self):
        """Test adding comments to webcams is successful"""
        category = models.Category.objects.create(name='Miasta')

        webcam_0 = models.Webcam.objects.create(
            name='Webcam 0',
            description='description 0',
            url='some url 0',
            thumbnail_url='some thumbnail 0 url',
            latitude=0.001,
            longitude=0.002,
            category=category,
            country=self.country,
            user_added=self.user,
        )
        webcam_1 = models.Webcam.objects.create(
            name='Webcam 1',
            description='description 1',
            url='some url 1',
            thumbnail_url='some thumbnail 1 url',
            latitude=0.006,
            longitude=0.009,
            category=category,
            country=self.country,
            user_added=self.user,
        )

        webcam_0_comment_0 = models.Comment.objects.create(
            content='Comment 0 to webcam 0',
            user_added=self.user,
            webcam=webcam_0,
        )
        webcam_0_comment_1 = models.Comment.objects.create(
            content='Comment 1 to webcam 0',
            user_added=self.user,
            webcam=webcam_0,
        )
        webcam_1_comment_0 = models.Comment.objects.create(
            content='Comment 0 to webcam 1',
            user_added=self.user,
            webcam=webcam_1,
        )
        webcam_1_comment_1 = models.Comment.objects.create(
            content='Comment 1 to webcam 1',
            user_added=self.user,
            webcam=webcam_1,
        )

        self.assertQuerySetEqual(
            webcam_0.comment_set.all(),
            [webcam_0_comment_0, webcam_0_comment_1],
            ordered=False,
            msg='Comments to webcam are not added properly'
        )

        self.assertQuerySetEqual(
            webcam_1.comment_set.all(),
            [webcam_1_comment_0, webcam_1_comment_1],
            ordered=False,
            msg='Comments to webcam are not added properly'
        )
