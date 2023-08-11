from django.urls import include, path
from djoser.views import UserViewSet
from knox import views
from rest_framework.routers import DefaultRouter

from accounts.views import CustomTokenCreateView

app_name = "accounts"
router = DefaultRouter()
router.register("users", UserViewSet)
urlpatterns = [
    path("", include(router.urls)),
    # * using Djoser and Knox for login mechanism
    path("login/", CustomTokenCreateView.as_view(), name="login"),
    path(r"logout/", views.LogoutView.as_view(), name="knox_logout"),
    path(r"logoutall/", views.LogoutAllView.as_view(), name="knox_logoutall"),
]
