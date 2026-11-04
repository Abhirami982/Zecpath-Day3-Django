from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path("register/", views.register, name="register"),
    path(
        "register/success/",
        views.register_success,
        name="register_success",
    ),
    path(
        "api/signup/",
        views.SignupAPIView.as_view(),
        name="api_signup",
    ),

    path(
        "api/login/",
        TokenObtainPairView.as_view(),
        name="api_login",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/protected/",
        views.ProtectedAPIView.as_view(),
        name="protected_api",
    ),
    
]
