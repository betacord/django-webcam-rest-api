from locations.models import Continent, Country


def get_sample_continent(continent_name):
    """Returns sample continent"""
    return Continent.objects.create(name=continent_name)


def get_sample_country(country_name, continent):
    """Returns sample continent"""
    return Country.objects.create(name=country_name, continent=continent)
