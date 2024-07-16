from django.urls import include, path
from rest_framework import routers

from api.v1.views import PetViewSet

router = routers.DefaultRouter()
router.register(r"pets", PetViewSet, basename="pet")

urlpatterns = [
    path("", include(router.urls)),
]
