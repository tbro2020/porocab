from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.db.models import signals
from django.dispatch import receiver

from service.models import Ride
from core.models import User

@receiver(signals.post_save, sender=Ride)
def post_save_ride(sender, instance, created, **kwargs):
    async_to_sync(get_channel_layer().group_send)('ride_{}'.format(instance.id), {
        'type': 'broadcast',
        'payload': instance.serialized
    })

