from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.db.models import signals
from django.dispatch import receiver
from service.models import Ride
from core.tasks import drivers

from djmoney.models.fields import MoneyField
from django.conf import settings
from djmoney.money import Money


@receiver(signals.pre_save, sender=Ride)
def pre_save_ride(sender, instance, **kwargs):
    price = instance.duration_in_minutes*settings.PRICE_PER_MINUTE
    price = Money(price, settings.DEFAULT_CURRENCY)
    instance.cost = price

@receiver(signals.post_save, sender=Ride)
def post_save_ride(sender, instance, created, **kwargs):
    async_to_sync(get_channel_layer().group_send)('ride_{}'.format(instance.id), {
        'type': 'broadcast',
        'payload': instance.serialized
    })
    if not created and instance.status != 'pending': return

    # run task async
    drivers.delay(instance.id)
        

