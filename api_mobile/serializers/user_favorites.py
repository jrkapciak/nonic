from rest_framework import serializers

from api_mobile.serializers.beers import BeerSerializer
from nonic.models import UserFavorite


class UserFavoriteBeerSerializer(serializers.ModelSerializer):
    beer = BeerSerializer()

    class Meta:
        model = UserFavorite
        fields = ("beer",)
