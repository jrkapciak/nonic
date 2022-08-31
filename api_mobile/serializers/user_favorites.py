from rest_framework import serializers
from nonic.models import UserFavorite
from api_mobile.serializers.beers import BeerSerializer

class UserFavoriteBeerSerializer(serializers.ModelSerializer):
    beer = BeerSerializer()

    class Meta:
        model = UserFavorite
        fields = ("beer",)