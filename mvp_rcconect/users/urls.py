from django.urls import path, include
from dj_rest_auth.views import UserDetailsView
from rest_framework import routers

from users import views

app_name = 'users'

router = routers.SimpleRouter()
router.register('users', viewset=views.UserViewSet)
router.register(r'profile', viewset=views.UserDetailViewSet)
router.register(r'phone', viewset=views.PhoneViewSet)
router.register(r'link', viewset=views.LinkViewSet)
router.register(r'document', viewset=views.DocumentViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
]
