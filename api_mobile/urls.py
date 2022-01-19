from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"beers", views.BeerViewSet, basename="beers"),
router.register(r"styles", views.StyleViewSet, basename="styles"),
urlpatterns = router.urls
