from rest_framework import serializers

from api_mobile.serializers.manufacture import ManufactureSerializer
from nonic.models import UserFavorite


class UserFavoriteBeerSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="beer.id")
    style = serializers.StringRelatedField(source="beer.style", read_only=True, many=True)
    name = serializers.CharField(source="beer.name")
    code = serializers.CharField(source="beer.code")
    alcohol = serializers.FloatField(source="beer.alcohol")
    thumbnail = serializers.URLField(source="beer.thumbnail")
    country = serializers.CharField(source="beer.country")
    rating_count = serializers.IntegerField(source="beer.rating_count")
    favorites_count = serializers.IntegerField(source="beer.favorites_count")
    rating = serializers.DecimalField(
        source="beer.rating", max_digits=3, decimal_places=2, coerce_to_string=False, required=False
    )
    manufactured_by = ManufactureSerializer(
        source="beer.manufactured_by",
        required=False,
        read_only=True,
    )

    class Meta:
        model = UserFavorite
        fields = (
            "id",
            "name",
            "code",
            "manufactured_by",
            "alcohol",
            "style",
            "thumbnail",
            "country",
            "rating",
            "rating_count",
            "favorites_count",
        )
