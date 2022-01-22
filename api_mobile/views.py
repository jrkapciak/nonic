from rest_framework import viewsets

from nonic import models as nonic_models

from . import serializers
from .filters import BeerFilter


class BeerViewSet(viewsets.ModelViewSet):
    paginate_by = 10
    queryset = nonic_models.Beer.objects.all()
    serializer_class = serializers.BeerSerializer
    filter_class = BeerFilter
    lookup_field = 'code'


class StyleViewSet(viewsets.ModelViewSet):
    paginate_by = 10
    queryset = nonic_models.Style.objects.all()
    serializer_class = serializers.StylesSerializer
