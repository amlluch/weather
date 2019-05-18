from django.db import models

# Create your models here.


class Station(models.Model):

    latlon = models.CharField(max_length=41, unique=True, null=False, blank=False)
    region = models.CharField(max_length=50, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    locality = models.CharField(max_length=200, null=True, blank=True)
    altitude = models.IntegerField(null=True, blank=True)


class DataWeather(models.Model):

    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=62, unique=True, null=False, blank=False)
    timestamp = models.DateTimeField()
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    wind_address = models.CharField(max_length=3, null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    pressure = models.IntegerField(null=True, blank=True)
    sun = models.IntegerField(null=True, blank=True)
    rain = models.FloatField(null=True, blank=True)

