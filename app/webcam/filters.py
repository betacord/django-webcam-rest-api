import django_filters

from locations.models import Country, Continent
from webcam.models import Category, Webcam


class WebcamFilter(django_filters.rest_framework.FilterSet):
    """Filers for webcam list"""
    category = django_filters.ModelMultipleChoiceFilter(to_field_name='id', queryset=Category.objects.all())
    country = django_filters.ModelMultipleChoiceFilter(to_field_name='id', queryset=Country.objects.all())
    continent = django_filters.ModelMultipleChoiceFilter(
        to_field_name='id',
        queryset=Continent.objects.all(),
        method='filter_continent'
    )

    def filter_continent(self, queryset, to_field_name, value):
        """Method returning filtered queryset by continent"""
        if value:
            return queryset.filter(country__continent__in=value)

        return queryset

    class Meta:
        model = Webcam
        fields = ('id', 'name', 'category', 'country', 'continent', 'user_added', )
