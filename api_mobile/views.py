from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from nonic import models as nonic_models
from rest_framework.decorators import action
from rest_framework.response import Response

from nonic.models import BeerRating
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
    def favorite(self, request):
        beer = self.get_object()
        if request.method == "post":
            beer.mark_as_favorite(self.request.user)
            response_status = status.HTTP_201_CREATED
        else:
            beer.remove_favorite(self.request.user)
            response_status = status.HTTP_204_NO_CONTENT
        return Response(status=response_status)

    @action(detail=True, methods=["post"])
    def rate(self, request, code):
        beer = self.get_object()
        rating = request.data.get("rating")
        BeerRating.objects.update_or_create(beer=beer, user=request.user, defaults={"rating": rating})
        beer.refresh_from_db()
        return Response(data=self.get_serializer(beer).data, status=status.HTTP_201_CREATED)


class StyleViewSet(viewsets.ReadOnlyModelViewSet):
    paginate_by = 10
    queryset = nonic_models.Style.objects.all()
    serializer_class = serializers.StylesSerializer
