from onesignal.model.notification import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.db.models import signals
from django.dispatch import receiver

from service.utils import price_the_ride
from service.tasks import drivers as drivers_task
from service.models import Ride, Vehicle

import onesignal
from onesignal.api import default_api

# Replace with your OneSignal App ID and REST API key
ONESIGNAL_APP_ID = 'f70c0348-5416-4739-83e0-a435d49e21b8'
ONESIGNAL_REST_API_KEY = 'MzZhZmNiYWYtMTdmYS00NTg3LThhZGYtM2I3YzJhYzNmNGYz'
configuration = onesignal.Configuration(app_key = ONESIGNAL_APP_ID, user_key = ONESIGNAL_REST_API_KEY)


@receiver(signals.pre_save, sender=Ride)
def pre_save_ride(sender, instance, **kwargs):
    if instance.cost.amount > 0: return
    instance.cost = price_the_ride(instance.vehicle, instance.duration_in_minutes)

@receiver(signals.post_save, sender=Ride)
def post_save_ride(sender, instance, created, **kwargs):
    async_to_sync(get_channel_layer().group_send)('ride_{}'.format(instance.id), {
        'type': 'broadcast',
        'payload': instance.serialized
    })
    if created:
        busies = Ride.objects.filter(status__in=['accepted', 'started']).values_list('driver__id', flat=True)
        drivers = Vehicle.objects.exclude(driver__in=busies).values_list('driver__id', flat=True)
        with onesignal.ApiClient(configuration) as api_client:
            notification = Notification(**{
                'app_id': ONESIGNAL_APP_ID,
                'include_external_user_ids': list(drivers),
                'contents': {'en': 'New ride request'},
                'headings': {'en': 'New ride request'}
            })
            default_api.DefaultApi(api_client).create_notification(notification)

    if not created and instance.status != 'pending': return
    drivers_task.delay(instance.id)