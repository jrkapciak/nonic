from rest_framework import serializers

from nonic import models


class ManufactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manufacturer
        fields = ("id", "name")


class BeerSerializer(serializers.ModelSerializer):
    style = serializers.StringRelatedField(read_only=True, many=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, coerce_to_string=False, required=False)
    manufactured_by = ManufactureSerializer(
        required=False,
        read_only=True,
    )
    lookup_field = "code"
    extra_kwargs = {"url": {"lookup_field": "code"}}

    class Meta:
        model = models.Beer
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


class BeerDetailSerializer(BeerSerializer):
    class Meta:
        model = models.Beer
        fields = BeerSerializer.Meta.fields + ("description",)


class StylesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Style
        fields = ("name",)


class BeerRatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()

    class Meta:
        model = models.BeerRating
        fields = ("id", "rating")
