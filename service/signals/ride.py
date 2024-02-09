from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from service.models import Ride, TypeOfVehicle
from django.db.models import signals
from django.dispatch import receiver
from core.models import Preference
from service.tasks import drivers

from django.utils.text import slugify
from django.conf import settings
from djmoney.money import Money

@receiver(signals.pre_save, sender=Ride)
def pre_save_ride(sender, instance, **kwargs):
    price = Preference.get('PRICE_PER_MINUTE') or settings.PRICE_PER_MINUTE
    prices = {
        vehicle[0]: Preference.get(slugify(vehicle[0])) or price
        for vehicle in TypeOfVehicle.choices
    }
    price = prices[instance.vehicle] or settings.PRICE_PER_MINUTE
    price = float(getattr(price, 'value', settings.PRICE_PER_MINUTE))
    
    price = instance.duration_in_minutes*price
    price = Money(price, settings.DEFAULT_CURRENCY)
    instance.cost = price

@receiver(signals.post_save, sender=Ride)
def post_save_ride(sender, instance, created, **kwargs):
    async_to_sync(get_channel_layer().group_send)('ride_{}'.format(instance.id), {
        'type': 'broadcast',
        'payload': instance.serialized
    })
    
    if not created and instance.status != 'pending': return
    drivers.delay(instance.id)
        

