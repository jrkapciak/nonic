from rest_framework import serializers

from nonic import models


class StylesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Style
        fields = ("name",)