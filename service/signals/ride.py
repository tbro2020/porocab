from django.db.models import signals
from django.dispatch import receiver

from service.tasks.new_ride import broadcast_new_ride_to_driver
from service.utils import price_the_ride
from service.models import Ride
import sentry_sdk
import requests


# Replace with your OneSignal App ID and REST API key
ONESIGNAL_APP_ID = 'f70c0348-5416-4739-83e0-a435d49e21b8'
ONESIGNAL_REST_API_KEY = 'MzZhZmNiYWYtMTdmYS00NTg3LThhZGYtM2I3YzJhYzNmNGYz'
ONESIGNAL_USER_KEY = 'MTljZDY0ZjAtZjdjZC00MDUxLWJiZGUtMTc4OWIzOTIwY2I3'

ONE_SIGNAL_HEADERS = {
    "Authorization": f"Basic {ONESIGNAL_REST_API_KEY}",
    "accept": "application/json",
    "content-type": "application/json"
}

ONE_SIGNAL_PAYLOAD_NEW_RIDE_TO_DRIVER = {
    "app_id": ONESIGNAL_APP_ID,
    "filters": [
        {"field": "tag", "key": "user_type", "relation": "=", "value": "driver"}
    ],
    "contents": {"en": "Nouvelle demande de course"},
    "headings": {"en": "Nouvelle course en attente"},
}

@receiver(signals.pre_save, sender=Ride)
def pre_save_ride(sender, instance, **kwargs):
    instance.cost = price_the_ride(instance.vehicle, instance.duration_in_minutes)

@receiver(signals.post_save, sender=Ride)
def post_save_ride(sender, instance, created, **kwargs):
    if not created: return
    try:
        broadcast_new_ride_to_driver.delay(instance.id)
        requests.post("https://onesignal.com/api/v1/notifications", headers=ONE_SIGNAL_HEADERS, json=ONE_SIGNAL_PAYLOAD_NEW_RIDE_TO_DRIVER)
    except Exception as e:
        sentry_sdk.capture_exception(e)