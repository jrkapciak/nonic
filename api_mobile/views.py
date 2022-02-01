from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from nonic import models as nonic_models
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers
from .filters import BeerFilter


class BeerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    paginate_by = 10
    queryset = nonic_models.Beer.objects.all()
    serializer_class = serializers.BeerSerializer
    filter_class = BeerFilter
    lookup_field = "code"

    @action(detail=True, methods=["post", "delete"])
    def favorite(self, request, pk=None):
        beer = self.get_object()
        if request.method == "post":
            beer.mark_as_favorite(self.request.user)
            response_status = status.HTTP_201_CREATED
        else:
            beer.remove_favorite(self.request.user)
            response_status = status.HTTP_204_NO_CONTENT
        return Response(status=response_status)


class StyleViewSet(viewsets.ReadOnlyModelViewSet):
    paginate_by = 10
    queryset = nonic_models.Style.objects.all()
    serializer_class = serializers.StylesSerializer
