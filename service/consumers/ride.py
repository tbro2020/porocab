from channels.generic.websocket import JsonWebsocketConsumer
from django.shortcuts import get_object_or_404
from service.models import Ride

from asgiref.sync import async_to_sync, sync_to_async

class RideConsumer(JsonWebsocketConsumer):
    def connect(self):
        pk = self.scope.get('url_route').get('kwargs').get('pk')
        self.room_group_name = 'ride_{}'.format(pk)
        self.obj = get_object_or_404(Ride, id=pk)
        self.accept()

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'broadcast',
            'payload': self.obj.serialized
        })
    
    def disconnect(self, close_code):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    def broadcast(self, payload):
        self.send_json(payload.get('payload'))
