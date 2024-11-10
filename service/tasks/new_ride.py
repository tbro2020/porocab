from service.models import Vehicle, Ride, RideStatus
from django.contrib.gis.measure import Distance
from django.conf import settings
from celery import shared_task

import pusher
import time

pusher_client = pusher.Pusher(**{
    'app_id': settings.PUSHER_APP_ID,
    'key': settings.PUSHER_KEY,
    'secret': settings.PUSHER_SECRET,
    'cluster': settings.PUSHER_CLUSTER,
    'ssl': True
})

@shared_task
def broadcast_new_ride_to_driver(ride_pk):
    waiting_time = 5
    current, max = 0, 5
    event_name = 'ride'

    ride = Ride.objects.get(pk=ride_pk)
    # drivers = Vehicle.objects.filter(last_know_location__dwithin=(ride.pick_up_location, Distance(m=1000)))
    drivers = Vehicle.objects.all()
    
    while max >= current:
        if not drivers or ride.status != RideStatus.PENDING : break
        _drivers = drivers.values_list('driver', flat=True)

        pusher_client.trigger([f'user-{driver}' for driver in _drivers], event_name, ride.serialized)
        drivers = drivers.all()
        ride.refresh_from_db()
        time.sleep(waiting_time)
        current += 1
        
    # update ride status to end the broadcasting
    ride.status = RideStatus.CANCELLED
    ride.save()
        