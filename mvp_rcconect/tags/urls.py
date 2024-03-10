from rest_framework import routers

from tags.views import TagViewSet

router = routers.SimpleRouter()
router.register(r'', viewset=TagViewSet)

urlpatterns = router.urls