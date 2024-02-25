from service.models import TypeOfVehicle
from django.utils.text import slugify
from djmoney.money import Money

from core.models import Preference
from django.conf import settings


def price_the_ride(vehicle, duration_in_minutes):
    price = Preference.get('PRICE_PER_MINUTE') or settings.PRICE_PER_MINUTE
    prices = {
        vehicle[0]: Preference.get(slugify(vehicle[0])) or price
        for vehicle in TypeOfVehicle.choices
    }

    price = prices[vehicle] or settings.PRICE_PER_MINUTE
    price = float(getattr(price, 'value', settings.PRICE_PER_MINUTE))

    price = duration_in_minutes*price
    return Money(price, settings.DEFAULT_CURRENCY)