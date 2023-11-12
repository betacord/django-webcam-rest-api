from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models import User
from webcam.models import Webcam
from webcam.serializers import WebcamSerializer
from webcam.tests.helpers import get_sample_random_webcam, get_sample_category, prepare_webcam_order_test_set

WEBCAM_LIST_URL = reverse('webcam:webcam_list')


class PublicWebcamAPITests(TestCase):
    """Test the public webcam API"""
    def setUp(self):
        self.public_client = APIClient()
        self.user = User.objects.create(
            email='janusz@polska.net',
            name='Janusz',
            is_active=True,
            is_staff=False,
        )
        self.sample_webcams = [
            get_sample_random_webcam(
                user=self.user,
                latitude=0.001,
                longitude=0.002,
                category=get_sample_category('rnd'),
            ),
            get_sample_random_webcam(
                user=self.user,
                latitude=0.001,
                longitude=0.002,
                category=get_sample_category('rnd'),
            ),
        ]

    def test_all_webcams_returned_correctly(self):
        """Test getting all webcams is successful"""
        res = self.public_client.get(WEBCAM_LIST_URL)
        serialized_webcams = WebcamSerializer(self.sample_webcams, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(res.data['results'], serialized_webcams.data, msg='Webcam list is not equal')

    def test_webcams_filtered_by_radius_of_location_are_returned_properly(self):
        """Test getting webcams in provided radius is successful"""
        webcams = [
            get_sample_random_webcam(
                user=self.user,
                latitude=-11.699428161432769,
                longitude=43.25321062572751,
                category=get_sample_category('rnd'),
            ),
            get_sample_random_webcam(
                user=self.user,
                latitude=-11.694825575392017,
                longitude=43.254464797815245,
                category=get_sample_category('rnd'),
            ),
            get_sample_random_webcam(
                user=self.user,
                latitude=40.37196375137453,
                longitude=49.85955728481766,
                category=get_sample_category('rnd'),
            ),
        ]

        res = self.public_client.get(
            WEBCAM_LIST_URL,
            {
                'user_lat': -11.6994281000000000,
                'user_lon': 43.25321000000000,
                'max_radius': 10,
            }
        )

        serialized_webcams = WebcamSerializer(webcams[:2], many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            serialized_webcams.data,
            msg='Webcam list filtered by location and radius is not equal'
        )

    def test_webcams_filtered_by_incomplete_params_of_radius_of_location_are_returned_properly_as_full_list(self):
        """
        Test getting webcams by passing incomplete set of get query params for filtering webcams in radius is successful
        """
        res_without_lat = self.public_client.get(
            WEBCAM_LIST_URL,
            {
                'user_lon': 43.25321000000000,
                'max_radius': 10,
            }
        )

        res_without_lon = self.public_client.get(
            WEBCAM_LIST_URL,
            {
                'user_lat': 43.25321000000000,
                'max_radius': 10,
            }
        )

        res_without_max_radius = self.public_client.get(
            WEBCAM_LIST_URL,
            {
                'user_lat': 43.25321000000000,
                'user_lon': 41.25321000000000,
            }
        )

        self.assertEqual(res_without_lat.status_code, status.HTTP_200_OK)
        self.assertEqual(res_without_lon.status_code, status.HTTP_200_OK)
        self.assertEqual(res_without_max_radius.status_code, status.HTTP_200_OK)

        self.assertEqual(
            res_without_lat.data['count'],
            len(self.sample_webcams),
            msg='Webcam list filtered by incomplete location and radius is not correct'
        )
        self.assertEqual(
            res_without_lon.data['count'],
            len(self.sample_webcams),
            msg='Webcam list filtered by incomplete location and radius is not correct'
        )
        self.assertEqual(
            res_without_max_radius.data['count'],
            len(self.sample_webcams),
            msg='Webcam list filtered by incomplete radius parameter is not correct'
        )

    def test_webcam_filtered_by_id_is_returned_properly(self):
        """Test filtering webcams by provided id is successful"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'id': self.sample_webcams[0].id,
            },
        )

        serialized_webcam = WebcamSerializer(self.sample_webcams[:1], many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(res.data['results'], serialized_webcam.data, msg='Webcam filtered by id is not correct')

    def test_webcam_filtered_by_name_is_returned_properly(self):
        """Test filtering webcams by provided name is successful"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'name': self.sample_webcams[0].name,
            },
        )

        serialized_webcam = WebcamSerializer(self.sample_webcams[:1], many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(res.data['results'], serialized_webcam.data, msg='Webcam filtered by name is not correct')

    def test_webcam_filtered_by_category_id_is_returned_properly(self):
        """Test filtering webcams by provided category id is successful"""
        webcams = [
            get_sample_random_webcam(
                user=self.user,
                latitude=0.001,
                longitude=0.002,
                category=get_sample_category('rnd'),
            ),
            get_sample_random_webcam(
                user=self.user,
                latitude=0.001,
                longitude=0.002,
                category=get_sample_category('rnd1'),
            ),
        ]

        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'category': webcams[0].category.id,
            },
        )

        serialized_webcam = WebcamSerializer(webcams[:1], many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            serialized_webcam.data,
            msg='Webcam filtered by category id is not correct'
        )

    def test_webcam_filtered_by_country_id_is_returned_properly(self):
        """Test filtering webcams by provided country id is successful"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'country': self.sample_webcams[0].country.id,
            },
        )

        serialized_webcam = WebcamSerializer(self.sample_webcams[:1], many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            serialized_webcam.data,
            msg='Webcam filtered by country id is not correct'
        )

    def test_webcam_filtered_by_continent_id_is_returned_properly(self):
        """Test filtering webcams by user added id is successful"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'user_added': self.sample_webcams[0].user_added.id,
            },
        )

        serialized_webcam = WebcamSerializer(self.sample_webcams, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            serialized_webcam.data,
            msg='Webcam filtered by continent id is not correct'
        )

    def test_webcam_found_by_full_name_using_search_engine_is_returned_properly(self):
        """Test searching webcams by full name"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'search': self.sample_webcams[0].name,
            },
        )

        serialized_webcam = WebcamSerializer(self.sample_webcams[:1], many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            serialized_webcam.data,
            msg='Webcam filtered by continent id is not correct'
        )

    def test_webcam_found_by_part_of_name_using_search_engine_is_returned_properly(self):
        """Test searching webcams by part of name"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'search': self.sample_webcams[0].name[1:7],
            },
        )

        serialized_webcam = WebcamSerializer(self.sample_webcams[:1], many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            serialized_webcam.data,
            msg='Webcam filtered by continent id is not correct'
        )

    def test_webcam_found_by_part_of_description_using_search_engine_is_returned_properly(self):
        """Test searching webcams by part of description"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'search': self.sample_webcams[0].description[3:11],
            },
        )

        serialized_webcam = WebcamSerializer(self.sample_webcams[:1], many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            serialized_webcam.data,
            msg='Webcam filtered by continent id is not correct'
        )

    def test_search_webcam_by_non_existing_name_and_description_should_return_empty_list(self):
        """Test searching webcam by non-existing name and description"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'search': 'non-existing text phrase',
            },
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 0)

    def test_webcam_found_by_part_of_category_name_using_search_engine_is_returned_properly(self):
        """Test searching webcams by a part of category name"""
        webcams = [
            get_sample_random_webcam(
                user=self.user,
                latitude=0.001,
                longitude=0.002,
                category=get_sample_category('random_cat'),
            ),
            get_sample_random_webcam(
                user=self.user,
                latitude=0.001,
                longitude=0.002,
                category=get_sample_category('rnd11222'),
            ),
        ]

        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'search': webcams[0].category.name[1:5],
            },
        )

        serialized_webcam = WebcamSerializer(webcams[:1], many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            serialized_webcam.data,
            msg='Webcam filtered by continent id is not correct'
        )

    def test_webcam_found_by_part_of_country_name_using_search_engine_is_returned_properly(self):
        """Test searching webcams by a part of country name"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'search': self.sample_webcams[0].country.name[1:5],
            },
        )

        serialized_webcam = WebcamSerializer(self.sample_webcams[:1], many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            serialized_webcam.data,
            msg='Webcam filtered by continent id is not correct'
        )

    def test_webcam_found_by_part_of_continent_name_using_search_engine_is_returned_properly(self):
        """Test searching webcams by a part of continent name"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'search': self.sample_webcams[0].country.continent.name[1:5],
            },
        )

        serialized_webcam = WebcamSerializer(self.sample_webcams[:1], many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            serialized_webcam.data,
            msg='Webcam filtered by continent id is not correct'
        )

    def test_webcam_found_by_part_of_user_name_using_search_engine_is_returned_properly(self):
        """Test searching webcams by a part of user's name"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'search': self.sample_webcams[0].user_added.name[1:5],
            },
        )

        serialized_webcam = WebcamSerializer(self.sample_webcams, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            serialized_webcam.data,
            msg='Webcam filtered by continent id is not correct'
        )

    def test_webcam_order_by_date_added_asc(self):
        """Test ordering webcams by date added ascending"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'ordering': 'date_added',
            },
        )

        webcams_serialized = WebcamSerializer(Webcam.objects.order_by('date_added'), many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            webcams_serialized.data,
            msg='Failed test ordering webcams by date added ascending'
        )

    def test_webcam_order_by_date_added_desc(self):
        """Test ordering webcams by date added descending"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'ordering': '-date_added',
            },
        )

        webcams_serialized = WebcamSerializer(Webcam.objects.order_by('-date_added'), many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            webcams_serialized.data,
            msg='Failed test ordering webcams by date added descending'
        )

    def test_webcam_order_by_category_name_desc(self):
        """Test ordering webcams by category name descending"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'ordering': '-category__name',
            },
        )

        webcams_serialized = WebcamSerializer(Webcam.objects.order_by('-category__name'), many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            webcams_serialized.data,
            msg='Failed test ordering webcams by category name descending'
        )

    def test_webcam_order_by_continent_name_asc(self):
        """Test ordering webcams by continent name ascending"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'ordering': 'country__continent__name',
            },
        )

        webcams_serialized = WebcamSerializer(Webcam.objects.order_by('country__continent__name'), many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            webcams_serialized.data,
            msg='Failed test ordering webcams by continent name ascending'
        )

    def test_webcam_order_by_continent_country_asc_date_added_desc(self):
        """Test ordering webcams by continent name ascending"""
        res = self.client.get(
            WEBCAM_LIST_URL,
            {
                'ordering': 'country__continent__name,country__name,-date_added',
            },
        )

        webcams_serialized = WebcamSerializer(
            Webcam.objects.order_by(
                'country__continent__name',
                'country__name',
                '-date_added'
            ),
            many=True,
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            res.data['results'],
            webcams_serialized.data,
            msg='Failed test ordering webcams by continent and country name ascending and date added descending'
        )
