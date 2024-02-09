from django.db.models import signals
from django.dispatch import receiver

from service.models import Invoice, TypeOfVehicle
from djmoney.money import Money

from django.utils.text import slugify
from core.models import Preference
from django.conf import settings

@receiver(signals.pre_save, sender=Invoice)
def pre_save_invoice(sender, instance, **kwargs):
    price = Preference.get('PRICE_PER_MINUTE') or settings.PRICE_PER_MINUTE
    prices = {
        vehicle[0]: Preference.get(slugify(vehicle[0])) or price
        for vehicle in TypeOfVehicle.choices
    }
    price = prices[instance.vehicle] or settings.PRICE_PER_MINUTE
    price = float(getattr(price, 'value', settings.PRICE_PER_MINUTE))
    
    price = instance.duration_in_minutes*price
    price = Money(price, settings.DEFAULT_CURRENCY)
    instance.price = price