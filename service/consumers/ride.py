from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from service.models import Ride

class Ride(AsyncJsonWebsocketConsumer):
    async def connect(self):
        pk = self.scope.get('url_route').get('kwargs').get('pk')
        self.room_group_name = 'ride_{}'.format(pk)
        self.obj = get_object_or_404(Ride, id=pk)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def broadcast(self, payload):
        await self.send_json(payload)
