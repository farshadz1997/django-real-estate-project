from django.urls import path
from . import viewsets as api_viewsets

app_name = "users_api"

urlpatterns = [
    path("api/login/", api_viewsets.LoginAPI.as_view(), name="api_login"),
    path("api/register/", api_viewsets.RegisterAPI.as_view(), name="api_register"),
    path("api/profile/", api_viewsets.ProfileAPI.as_view(), name="api_profile"),
    path("api/user/", api_viewsets.UserAPI.as_view(), name="api_user"),
    path("api/change-password/", api_viewsets.ChangePasswordAPI.as_view(), name="api_change_password"),
]
