from rest_framework import routers

from .views import EventViewSet, EventImageViewSet, PostViewSet

router = routers.SimpleRouter()
router.register(r'', viewset=EventViewSet)
router.register(r'images', viewset=EventImageViewSet)
router.register(r'posts', viewset=PostViewSet)


urlpatterns = router.urls
