from django.urls import path, include
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import LoginAPIView, RedirectSocial

app_name = "authenticate"


urlpatterns = [
    path("register/", UserViewSet.as_view({"post": "create"}), name="register"),
    path("users/", UserViewSet.as_view({"get": "list"})),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("verify/", TokenVerifyView.as_view(), name="verify"),
    path(
        "activation/<str:uid>/<str:token>/",
        UserViewSet.as_view({"post": "activation"}),
        name="activation",
    ),
    path(
        "resend-activation/",
        UserViewSet.as_view({"post": "resend_activation"}),
        name="resend_activation",
    ),
    path(
        "reset-password/",
        UserViewSet.as_view({"post": "reset_password"}),
        name="reset_password",
    ),
    path(
        "reset-password-confirm/<str:uid>/<str:token>/",
        UserViewSet.as_view({"post": "reset_password_confirm"}),
        name="reset_password_confirm",
    ),
    # path(
    #     "login/facebook/callback/",
    #     FacebookLogin.as_view(),
    #     name="login-with-facebook",
    # ),
    path('accounts/profile/', RedirectSocial.as_view()),
    path('social/', include('djoser.social.urls')),
]
