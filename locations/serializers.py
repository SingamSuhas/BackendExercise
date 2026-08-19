from rest_framework import serializers
from .models import Country,State,City

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model=Country
        fields=["id","name","country_code","curr_symbol","phone_code","user"]
        read_only_fields=["id","user"]

    def create(self,validated_data):
        user=self.context["request"].user
        return Country.objects.create(user=user,**validated_data)

class StateSerializer(serializers.ModelSerializer):
    my_country__name=serializers.SerializerMethodField()
    my_country__my_user__name=serializers.SerializerMethodField()

    class Meta:
        model=State
        fields=["id","name","state_code","gst_code","country","my_country__name","my_country__my_user__name"]
        read_only_fields=["id"]
    def validate_country(self,country):
        user=self.context["request"].user
        if country.user_id!=user.id:
            raise serializers.ValidationError("You cannot user a country owned by another user.")
        return country
    def get_my_country__name(self,obj):
        return obj.country.name
    def get_my_country__my_user__name(self,obj):
        return obj.country.user.first_name
    def create(self,validated_data):
        print("VALIDATED DATA:",validated_data)
        state=State.objects.create(**validated_data)
        return state

class CitySerializer(serializers.ModelSerializer):
    my_state__name=serializers.SerializerMethodField()
    class Meta:
        model=City
        fields=["id","name","city_code","phone_code","population","avg_age","num_of_adult_males","num_of_adult_females","state","my_state__name"]
        read_only_fields=["id","my_state__name"]

    def validate_state(self,state):
        user=self.context["request"].user
        if state.country.user_id!=user.id:
            raise serializers.ValidationError("You cannot use a state owned by another user.")
        return state
    def get_my_state__name(self,obj):
        return obj.state.name

    def validate(self,attrs):
        population=attrs.get("population",getattr(self.instance,"population",None))
        adult_males=attrs.get("num_of_adult_males",getattr(self.instance,"num_of_adult_males",None))
        adult_females=attrs.get("num_of_adult_females",getattr(self.instance,"num_of_adult_females",None))

        if None not in [population,adult_males,adult_females]:
            total_adults=adult_males+adult_females

            if population<=total_adults:
                raise serializers.ValidationError({
                    "population":"Population must be greater than the total number of adult males and females"
                })

        state=attrs.get("state",getattr(self.instance,"state",None))
        name=attrs.get("name",getattr(self.instance,"name",None))

        if state and name:
            duplicate_city_exists=City.objects.filter(
                state=state,
                name=name
            ).exclude(
                pk=getattr(self.instance,"pk",None)
            ).exists()

            if duplicate_city_exists:
                raise serializers.ValidationError({
                    "name":"A city with this name already exists within this state"
                })

        return attrs