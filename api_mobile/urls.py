from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from api_mobile.views.beers import BeerViewSet
from api_mobile.views.styles import StyleViewSet
from api_mobile.views.user_favorites import UserFavoritesBeersViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Nonic API",
        default_version="v1",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register("beers", BeerViewSet, basename="beers")
router.register("styles", StyleViewSet, basename="styles")
router.register("user/favorites", UserFavoritesBeersViewSet, basename="user_favorites")

urlpatterns = router.urls

urlpatterns += [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
