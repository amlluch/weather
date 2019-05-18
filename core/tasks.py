
from celery import shared_task


@shared_task
def celery_test(param):
    return param * 2


@shared_task
def add_element(instance):
    with open('prueba', 'a') as guarda:
        guarda.write(instance.station.locality)

