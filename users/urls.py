from django.urls import path
from .views import(UserListCreateView,UserRetriveUpdateDestroyView,SignInView,SignOutView,)
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns=[
    path("",UserListCreateView.as_view(),name="user-list-create"),
    path("<int:pk>/",UserRetriveUpdateDestroyView.as_view(),name="user-detail"),

]