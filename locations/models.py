from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
# Create your models here.
class Country(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    country_code=models.CharField(max_length=100,unique=True)
    curr_symbol=models.CharField(max_length=10)
    phone_code=models.CharField(max_length=10,unique=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="countries")

    def __str__(self):
        return self.name


class State(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    state_code=models.CharField(max_length=10,unique=True)
    gst_code=models.CharField(max_length=10,unique=True)
    country=models.ForeignKey(Country,on_delete=models.CASCADE,related_name="states")

    class Meta:
        constraints=[models.UniqueConstraint(fields=["country","name"],name="unique_state_name_per_country"),models.UniqueConstraint(fields=["country","state_code"],name="unique_state_code_per_country"),]

    def __str__(self):
        return self.name
    
class City(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    city_code=models.CharField(max_length=10)
    phone_code=models.CharField(max_length=10,unique=True)
    population=models.PositiveBigIntegerField()
    avg_age=models.PositiveIntegerField()
    num_of_adult_males=models.PositiveBigIntegerField()
    num_of_adult_females=models.PositiveBigIntegerField()
    state=models.ForeignKey(State,on_delete=models.CASCADE,related_name="cities")

    class Meta:
        constraints=[models.UniqueConstraint(fields=["state","name"],name="unique_city_name_per_state"),models.UniqueConstraint(fields=["state","city_code"],name="unique_city_code_per_state"),]

    def clean(self):
        total_adults=(self.num_of_adult_males+self.num_of_adult_females)
        if self.population<=total_adults:
            raise ValidationError({
                'population':("Population must be greater than the total number of adult males and females")
            })
    def save(self,*args,**kwargs):
        self.full_clean()
        super().save(*args,**kwargs)
    def __str__(self):
        return self.name