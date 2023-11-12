from random import randint

from locations.tests.helpers import get_sample_country, get_sample_continent
from user.tests.test_api import create_user
from webcam.models import Category, Webcam


def get_rnd_str(length):
    return ''.join([chr(randint(97, 123)) for _ in range(length)])


def get_sample_category(category_name):
    """Returns sample webcam category"""
    return Category.objects.create(name=category_name)


def get_sample_random_webcam(user, latitude, longitude, category):
    """Returns sample webcam"""
    return Webcam.objects.create(
        name=get_rnd_str(10),
        description=get_rnd_str(20),
        url=f'http://{get_rnd_str(40)}',
        thumbnail_url=f'http://{get_rnd_str(25)}',
        latitude=latitude,
        longitude=longitude,
        category=category,
        country=get_sample_country(get_rnd_str(10), get_sample_continent(get_rnd_str(12))),
        user_added=user,
    )


def get_sample_webcam(name, category_name, country_name, continent_name):
    """Returns sample webcam"""
    category = get_sample_category(category_name)

    return Webcam.objects.create(
        name=name,
        description='description',
        url='http://aaa.pl',
        thumbnail_url='http://a.pl/1.jpg',
        latitude=0.001,
        longitude=0.002,
        category=category,
        country=get_sample_country(country_name, get_sample_continent(continent_name)),
        user_added=create_user(email='donosy@policja.net', password='p4ss55', name='test name'),
    )


def prepare_webcam_order_test_set(n):
    """Creates n webcams with random values of attributes"""
    for i in range(n):
        rnd_username = get_rnd_str(20)
        get_sample_random_webcam(
            user=create_user(
                email=f'{rnd_username}@polska.net',
                name=rnd_username,
                is_active=True,
                is_staff=False,
            ),
            latitude=0.111,
            longitude=1.111,
            category=get_sample_category(get_rnd_str(15)),
        )
