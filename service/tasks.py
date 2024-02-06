from channels.layers import get_channel_layer
from service.models import Ride, RideStatus
from asgiref.sync import async_to_sync
from celery import shared_task
from time import sleep

@shared_task
def drivers(pk):
    channel_layer = get_channel_layer()
    ride = Ride.objects.get(id=pk)
    room = 'drivers-of-kinshasa'
    for _ in range(5):
        if ride.status != RideStatus.PENDING:
            break
        async_to_sync(channel_layer.group_send)(room, {'type': 'broadcast', 'payload': ride.serialized})
        ride.refresh_from_db()
        sleep(5)
    else:
        ride.status = RideStatus.CANCELLED
        ride.save()

        







    