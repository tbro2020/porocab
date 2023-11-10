from api.serializers import model_serializer_factory
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.db.models import signals
from django.dispatch import receiver

from service.models import Ride
from core.models import User

@receiver(signals.post_save, sender=Ride)
def post_saved(sender, instance, created, **kwargs):
    serializer = model_serializer_factory(instance._meta.model)
    serialized = serializer(instance, many=False)

    async_to_sync(get_channel_layer().group_send)(
        'ride_{}'.format(instance.id),
        {
            'type': 'broadcast', 
            'message': serialized.data
        }
    )

    if not instance.current_location: return
    users = [instance.client, instance.driver]
    users = [user.id for user in users if user]
    User.objects.filter(id__in=users).update(**{
        'last_known_position': instance.current_location
    })

