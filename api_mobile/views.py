from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from nonic import models as nonic_models
from rest_framework.decorators import action
from rest_framework.response import Response

from nonic.models import BeerRating, UserFavorite
from . import serializers
from .filters import BeerFilter
from .serializers import BeerRatingSerializer, BeerDetailSerializer


class BeerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    paginate_by = 10
    queryset = nonic_models.Beer.objects.all()
    serializer_class = serializers.BeerSerializer
    filter_class = BeerFilter
    lookup_field = "code"
    default_serializer_class = serializers.BeerSerializer
    serializers = {
        "list": serializers.BeerSerializer,
        "detail": serializers.BeerDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer_class)

    @action(detail=True, methods=["post", "delete"])
    def favorite(self, request, code):
        beer = self.get_object()
        if request.method == "POST":
            if UserFavorite.objects.filter(beer=beer, user=request.user).exists():
                return Response("Already added as favorite", status=status.HTTP_200_OK)
            UserFavorite.objects.create(beer=beer, user=request.user)
            response_status = status.HTTP_201_CREATED

        elif request.method == "DELETE":
            user_favorite = get_object_or_404(UserFavorite, **{"beer": beer, "user": request.user})
            user_favorite.delete()
            response_status = status.HTTP_204_NO_CONTENT

        return Response(status=response_status)

    @action(detail=True, methods=["post"])
    def rate(self, request, code):
        beer = self.get_object()
        beer_rating_serializer = BeerRatingSerializer(data=request.data)
        beer_rating_serializer.is_valid(raise_exception=True)
        BeerRating.objects.update_or_create(
            beer=beer, user=request.user, defaults={"rating": beer_rating_serializer.validated_data.get("rating")}
        )
        beer.refresh_from_db()
        return Response(data=self.get_serializer(beer).data, status=status.HTTP_201_CREATED)


class StyleViewSet(viewsets.ReadOnlyModelViewSet):
    paginate_by = 10
    queryset = nonic_models.Style.objects.all()
    serializer_class = serializers.StylesSerializer
