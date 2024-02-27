from rest_framework.routers import DefaultRouter, SimpleRouter

from config import settings
from service.api import viewsets

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register("clients", viewsets.ClientViewSet, basename="clients")
router.register("requests", viewsets.RequestViewSet, basename="requests")

urlpatterns = router.urls
