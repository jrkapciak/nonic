from rest_framework import viewsets

from api_mobile.serializers.user_favorites import UserFavoriteBeerSerializer
from nonic import models as nonic_models


class UserFavoritesBeersViewSet(viewsets.ModelViewSet):
    paginate_by = 10
    queryset = nonic_models.UserFavorite.objects.all()
    serializer_class = UserFavoriteBeerSerializer
