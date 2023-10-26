from rest_framework import serializers

from locations.models import Continent, Country


class ContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Continent
        fields = (
            'name',
        )


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            'name',
            'continent',
        )
