from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task

from api.serializers import model_serializer_factory
from service.models import Driver


@shared_task(name='drivers')
def drivers():
    serializer = model_serializer_factory(Driver)
    drivers = Driver.objects.all()

    serialized = serializer(drivers, many=True)
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)(
        'drivers',
        {
            'type': 'broadcast', 
            'message': serialized.data
        }
    )