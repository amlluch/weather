
from django.dispatch import receiver
from .models import DataWeather
from django.db.models.signals import post_save


@receiver(post_save, sender=DataWeather)
def new_weatherdata(sender, instance, created, **kwargs):
    if created:
        with open('nuevos', mode='a') as nuevo:
            nuevo.write(instance.station.locality + ' \t' + instance.timestamp + '\n')
