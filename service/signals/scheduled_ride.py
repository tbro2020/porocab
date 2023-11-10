from api.serializers import model_serializer_factory
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.db.models import signals
from django.dispatch import receiver

from service.models import ScheduledRide

@receiver(signals.post_save, sender=ScheduledRide)
def post_saved(sender, instance, created, **kwargs):
    # To Do: on status changed to success notify the driver for the ride
    return

