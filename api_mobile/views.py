from rest_framework import viewsets

from nonic import filters as nonic_filters
from nonic import models as nonic_models

from . import serializers


class BeerViewSet(viewsets.ModelViewSet):
    paginate_by = 10
    queryset = nonic_models.Beer.objects.all()
    serializer_class = serializers.BeerSerializer
    filter_class = nonic_filters.BeerFilter
