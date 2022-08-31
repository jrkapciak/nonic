from rest_framework import viewsets

from nonic import models as nonic_models

from api_mobile.serializers.styles import StylesSerializer


class StyleViewSet(viewsets.ModelViewSet):
    paginate_by = 10
    queryset = nonic_models.Style.objects.all()
    serializer_class = StylesSerializer