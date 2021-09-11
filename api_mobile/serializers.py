from rest_framework import serializers

from nonic import models


class BeerSerializer(serializers.ModelSerializer):
    style = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = models.Beer
        fields = (
            "name",
            "code",
            "description",
            "manufactured_by",
            "volume",
            "extract",
            "alcohol",
            "style",
            "thumbnail",
        )
