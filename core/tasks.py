from datetime import datetime
from celery import shared_task
from django.apps import apps

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from service.models import Ride
import time


@shared_task(name='daily')
def daily():
    qs = apps.get_model('core', 'job').objects.all()
    for obj in qs:
        try:
            print(obj.name, datetime.now())
            eval(obj.job, locals())
        except:
            pass


@shared_task
def drivers(ride):
    ride = Ride.objects.get(id=ride)
    while ride.status != 'pending':
        ride = Ride.objects.get(id=ride)
        async_to_sync(get_channel_layer().group_send)('drivers-of-kinshasa', {'type': 'broadcast', 'payload': ride.serialized})
        time.sleep(5)






    