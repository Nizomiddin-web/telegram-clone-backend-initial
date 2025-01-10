import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': "Websocket ulanishi muvafaqiyatli o'rnatildi"
        }))

    async def disconnect(self, code):
        print("Aloqa uzildi")

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        data = json.loads(text_data)
        message = data['message']+ ' bu serverga jonatildi'

        # xabarni qayta jo'natish
        await self.send(text_data=json.dumps({
            'message':message
        }))