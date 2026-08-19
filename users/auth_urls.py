from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignInView,SignOutView

urlpatterns=[
    path("signin/",SignInView.as_view(),name="signin"),
    path("signout/",SignOutView.as_view(),name="signout"),
    path("refresh/",TokenRefreshView.as_view(),name="token-refresh"),
]