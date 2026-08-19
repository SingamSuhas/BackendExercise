from django.urls import path
from .views import (CountryListCreateView,
                    CountryRetriveUpdateDestroyView,
                    StateListCreateView,
                    StateRetriveUpdateDestroyView,
                    CityListCreateView,
                    CityRetriverUpdateDestroyView,
                    CountryStateCityCreateView,
                    CountryStateCityRetriveUpdateDestroyView,
                    CountryStateCreateView,
                    CountryStateRetriveUpdateDestroyView)

urlpatterns=[
    path("countries/",CountryListCreateView.as_view(),name="country-list-create"),
    path("countries/<int:pk>/",CountryRetriveUpdateDestroyView.as_view(),name="country-detail"),
    path("countries/<int:country_id>/states/",CountryStateCreateView.as_view(),name="country-state-list-create"),
    path("countries/<int:country_id>/states/<int:pk>/",CountryStateRetriveUpdateDestroyView.as_view(),name="country-state-detail"),
    path("countries/<int:country_id>/states/<int:state_id>/cities/",CountryStateCityCreateView.as_view(),name="country-state-city-detail"),
    path("countries/<int:country_id>/states/<int:state_id>/cities/<int:pk>/",CountryStateCityRetriveUpdateDestroyView.as_view(),name="country-state-city-detail"),
    path("states/",StateListCreateView.as_view(),name="state-list-create"),
    path("states/<int:pk>/",StateRetriveUpdateDestroyView.as_view(),name="state-detail"),
    path("cities/",CityListCreateView.as_view(),name='city-list-create'),
    path("cities/<int:pk>/",CityRetriverUpdateDestroyView.as_view(),name="city-detail"),
]