from service.utils import price_the_ride
from django.db.models import signals
from django.dispatch import receiver
from service.models import Invoice

@receiver(signals.pre_save, sender=Invoice)
def pre_save_invoice(sender, instance, **kwargs):
    instance.price = price_the_ride(instance.vehicle, instance.duration_in_minutes)