from django.urls import path

from .views import (
    SignupAPIView,
    LoginView,
    LogoutView,
    ChangePasswordView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ProfileView
)

urlpatterns = [

    path(
        "signup/",
        SignupAPIView.as_view(),
        name="signup"
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout"
    ),

    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password"
    ),

    path(
        "reset-password/",
        PasswordResetRequestView.as_view(),
        name="reset-password"
    ),

    path(
        "reset-confirm/<uid>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="reset-confirm"
    ),
    path(
        "profile/",
        ProfileView.as_view(),
        name="profile"
    ),

]