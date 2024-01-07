from channels.generic.websocket import AsyncJsonWebsocketConsumer

class Drivers(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # locality = self.scope['url_path']['kwargs']['locality']
        self.room_group_name = 'drivers-of-kinshasa'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def broadcast(self, payload):
        await self.send_json(payload.get('payload'))