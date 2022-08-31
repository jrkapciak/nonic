from rest_framework import viewsets

from api_mobile.serializers.styles import StylesSerializer
from nonic import models as nonic_models


class StyleViewSet(viewsets.ModelViewSet):
    paginate_by = 10
    queryset = nonic_models.Style.objects.all()
    serializer_class = StylesSerializer
