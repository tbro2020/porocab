from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.db.models import signals
from django.dispatch import receiver

from service.models import Ride, RideStatus

@receiver(signals.post_save, sender=Ride)
def post_save_ride(sender, instance, created, **kwargs):
    async_to_sync(get_channel_layer().group_send)('ride_{}'.format(instance.id), {
        'type': 'broadcast',
        'payload': instance.serialized
    })
    if not created and instance.status != 'pending': return
    async_to_sync(get_channel_layer().group_send)('drivers-of-kinshasa', {
        'type': 'broadcast',
        'payload': instance.serialized
    })

