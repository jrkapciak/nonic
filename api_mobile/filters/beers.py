import django_filters

from nonic.models import Beer


class BeerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    code = django_filters.CharFilter(lookup_expr="icontains")
    style = django_filters.CharFilter(lookup_expr="icontains")
    country = django_filters.CharFilter(lookup_expr="icontains")
    alcohol = django_filters.NumberFilter(field_name="alcohol", lookup_expr="iexact")
    alcohol__lt = django_filters.NumberFilter(field_name="alcohol", lookup_expr="lt")
    alcohol__gt = django_filters.NumberFilter(field_name="alcohol", lookup_expr="gt")

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
            "country",
        )
