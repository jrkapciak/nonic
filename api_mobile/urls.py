from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"beers", views.BeerViewSet, basename="beers")
urlpatterns = router.urls
