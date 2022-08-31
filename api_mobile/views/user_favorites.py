from rest_framework import viewsets

from nonic import models as nonic_models

from api_mobile.serializers.user_favorites import UserFavoriteBeerSerializer


class UserFavoritesBeersViewSet(viewsets.ModelViewSet):
    paginate_by = 10
    queryset = nonic_models.UserFavorite.objects.all()
    serializer_class = UserFavoriteBeerSerializer