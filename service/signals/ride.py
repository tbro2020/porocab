from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.db.models import signals
from django.dispatch import receiver

from service.utils import price_the_ride
from service.tasks import drivers
from service.models import Ride

@receiver(signals.pre_save, sender=Ride)
def pre_save_ride(sender, instance, **kwargs):
    if instance.cost.amount > 0: return
    instance.cost = price_the_ride(instance.vehicle, instance.duration_in_minutes)

@receiver(signals.post_save, sender=Ride)
def post_save_ride(sender, instance, created, **kwargs):
    async_to_sync(get_channel_layer().group_send)('ride_{}'.format(instance.id), {
        'type': 'broadcast',
        'payload': instance.serialized
    })
    if not created and instance.status != 'pending': return
    drivers.delay(instance.id)
        

