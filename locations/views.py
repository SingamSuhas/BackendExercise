from django.shortcuts import get_object_or_404
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from .models import Country,State,City
from .serializers import (CountrySerializer,StateSerializer,CitySerializer)
# Create your views here.

class CountryListCreateView(ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Country.objects.all()
    serializer_class=CountrySerializer

    def get_queryset(self):
        user=self.request.user
        return Country.objects.filter(user=user)
    
class CountryRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Country.objects.all()
    serializer_class=CountrySerializer

    def get_queryset(self):
        return Country.objects.filter(user=self.request.user)

class StateListCreateView(ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=State.objects.all()
    serializer_class=StateSerializer

    def get_queryset(self):
        user=self.request.user
        return State.objects.select_related("country","country__user").filter(country__user=user)

class StateRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=State.objects.all()
    serializer_class=StateSerializer

    def get_queryset(self):
        return State.objects.filter(country__user=self.request.user)

class CityListCreateView(ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=City.objects.all()
    serializer_class=CitySerializer

    def get_queryset(self):
        return City.objects.filter(state__country__user=self.request.user)

class CityRetriverUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=City.objects.all()
    serializer_class=CitySerializer

    def get_queryset(self):
        return City.objects.filter(state__country__user=self.request.user)

class CountryStateCreateView(ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=StateSerializer

    def get_queryset(self):
        country_id=self.kwargs["country_id"]
        return State.objects.filter(country_id=country_id,country__user=self.request.user)

    def perform_create(self,serializer):
        country=get_object_or_404(
            Country,
            id=self.kwargs["country_id"],
            user=self.request.user
        )
        serializer.save(country=country)

class CountryStateRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=StateSerializer

    def get_queryset(self):
        country_id=self.kwargs["country_id"]
        return State.objects.filter(country_id=country_id,country__user=self.request.user)

class CountryStateCityCreateView(ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CitySerializer

    def get_queryset(self):
        country_id=self.kwargs["country_id"]
        state_id=self.kwargs["state_id"]
        return City.objects.filter(
            state_id=state_id,
            state__country_id=country_id,
            state__country__user=self.request.user
        )

    def perform_create(self,serializer):
        state=get_object_or_404(
            State,
            id=self.kwargs["state_id"],
            country_id=self.kwargs["country_id"],
            country__user=self.request.user
        )
        serializer.save(state=state)

class CountryStateCityRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CitySerializer

    def get_queryset(self):
        country_id=self.kwargs["country_id"]
        state_id=self.kwargs["state_id"]
        return City.objects.filter(
            state_id=state_id,
            state__country_id=country_id,
            state__country__user=self.request.user
        )