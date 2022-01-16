import django_filters

from .models import Beer


class BeerFilter(django_filters.FilterSet):
    class Meta:
        model = Beer
        fields = (
            "name",
            "code",
            "description",
            "manufactured_by",
            "volume",
            "extract",
            "alcohol",
            "style",
        )
