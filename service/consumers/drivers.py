from channels.generic.websocket import JsonWebsocketConsumer
from service.models import Ride, RideStatus
from asgiref.sync import async_to_sync
from django.utils import timezone
from datetime import timedelta

class Drivers(JsonWebsocketConsumer):
    def connect(self):
        self.room_group_name = 'drivers-of-kinshasa'
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

        twenty_minutes_ago = timezone.now() - timedelta(minutes=20)
        qs = Ride.objects.filter(**{
            'status': RideStatus.PENDING,
            'created_at__gte': twenty_minutes_ago
        })
        if not qs.exists(): return
        self.send_json(qs.first().serialized)

    def disconnect(self, close_code):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    def broadcast(self, payload):
        self.send_json(payload.get('payload'))