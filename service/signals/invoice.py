from django.db.models import signals
from django.dispatch import receiver

from service.models import Invoice
from djmoney.money import Money

from django.conf import settings

@receiver(signals.pre_save, sender=Invoice)
def pre_save_invoice(sender, instance, **kwargs):
    price = instance.duration_in_minutes*settings.PRICE_PER_MINUTE
    price = Money(price, settings.DEFAULT_CURRENCY)
    instance.price = price