from channels.generic.websocket import AsyncJsonWebsocketConsumer
from service.models import Driver

class Drivers(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'drivers'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        print('Disconnected')
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def broadcast(self, payload):
        await self.send_json(payload)