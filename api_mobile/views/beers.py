from rest_framework import viewsets

from nonic import models as nonic_models

from api_mobile import serializers
from api_mobile.filters.beers import BeerFilter


class BeerViewSet(viewsets.ModelViewSet):
    paginate_by = 10
    queryset = nonic_models.Beer.objects.all()
    serializer_class = serializers.BeerSerializer
    filter_class = BeerFilter