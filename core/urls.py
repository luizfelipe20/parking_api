from rest_framework import routers

from core.api import ParkingViewSet

router = routers.SimpleRouter()
router.register(r"parking", ParkingViewSet)
