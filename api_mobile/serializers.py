from rest_framework import serializers

from nonic import models


class ManufactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manufacturer
        fields = ("id", "name")


class BeerSerializer(serializers.ModelSerializer):
    style = serializers.StringRelatedField(read_only=True, many=True)
    manufactured_by = ManufactureSerializer(
        required=False,
        read_only=True,
    )

    class Meta:
        model = models.Beer
        fields = (
            "id",
            "name",
            "code",
            "description",
            "manufactured_by",
            "volume",
            "extract",
            "alcohol",
            "style",
            "thumbnail",
            "country",
            "rating",
            "rating_count",
        )
