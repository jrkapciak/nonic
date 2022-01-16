from rest_framework import serializers

from nonic import models


class ManufactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manufacturer
        fields = (
            'id',
            'name'
        )


class BeerSerializer(serializers.ModelSerializer):
    style = serializers.StringRelatedField(read_only=True, many=True)

    manufactured_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Manufacturer.objects.all(),
        required=False,
        source='manufactured_by',
    )
    manufactured_by = ManufactureSerializer(
        required=False,
        read_only=True,
    )

    class Meta:
        model = models.Beer
        fields = (
            "name",
            "code",
            "description",
            "manufactured_by",
            "manufactured_id",
            "volume",
            "extract",
            "alcohol",
            "style",
            "thumbnail",
        )
