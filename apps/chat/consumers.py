import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from django.contrib.auth.models import AnonymousUser
from djangochannelsrestframework.observer.generics import action


from chat.models import Chat, ChatParticipant
from chat.serializers import ChatSerializer, MessageSerializer, UserSerializer


class ChatConsumer(ObserverModelInstanceMixin,GenericAsyncAPIConsumer,AsyncJsonWebsocketConsumer):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = 'pk' #qidirish uchun asosiy kalit maydon

    async def connect(self):
        self.user = self.scope.get("user",AnonymousUser()) #foydalanuvchini olish
        self.chat_id = self.scope["url_route"]["kwargs"]["pk"] #Chat ID sini olish
        self.chat = await self.get_chat(self.chat_id) #chat obyektini olish
        print(self.chat,"ddjjjjjjjjjjjjjjjjjjjjjj")
        self.participants = await self.current_users(self.chat) #Hozirgi ishtirokchilarni olish

        #Agar foydalanuchi autentifikatsiyadan o'tmagan bo'lsa,ulanishni yopamiz
        if not self.user.is_authenticated:
            return await self.close()
        #Agar chat mavjud bo'lmasa,ulanishni yopamiz
        if not self.chat:
            return await self.close()
        #Agar foydalanuvchi chat ishtirokchisi bo'lmasa chatni yopamiz
        if self.user.id not in [self.chat.owner_id,self.chat.user_id]:
            return await self.close()

        # WebSocket guruhiga foydalanuvchini qo'shish
        await self.channel_layer.group_add(f"chat__{self.chat_id}",self.channel_name)
        await self.add_user_to_chat(self.chat_id) # Foydalanuvchini chatga qo'shish
        await self.accept() #Ulanishni qabul qilish
        await self.update_user_status(is_online=True) #Foydalanuvchi holatini yangilash
        await self.notify_users() #Barcha foydalanuvchilarga yangi ishtirokchilar haqida xabar berish
        await self.get_messages(self.chat_id) #Oldingi habarlarni olish

    #WebSocket uzilganda bajariladi
    async def disconnect(self, code):
        if self.user.is_authenticated:
            await self.remove_user_from_chat(self.chat_id) #Foydalanuvchini chatdan olib tashlash
            await self.update_user_status(is_online=False)
            await self.notify_users()
            await self.channel_layer.group_discard(
                f"chat__{self.chat_id}",self.channel_name
            )
        print("to'xtadi")
        await super().disconnect(code)

    #Barcha foydalanuvchilarga ishtirokchilar ro'yhatini yuborish
    async def notify_users(self):
        participants = await self.current_users(self.chat) #Hozirgi ishtirokchilarni olish
        users = await self.serialize_users(participants) #Ishtirokchilarni seriyalash
        await self.channel_layer.group_send(
            f"chat__{self.chat_id}",{"type":"update_users","users":users}
        )

    #Foydalanuvchilarni yangilash habarini yuborish
    async def update_users(self,event):
        await self.send_json({"users":event["users"]}) #Json Formatida yuborish

    # Xabarlarni olish uchun endpoint
    @action()
    async def get_messages(self,pk,**kwargs):
        messages = await self.fetch_messages(pk) #Habarlarni bazadan olish
        serialized_messages = await self.serialize_messages(messages)

        await self.send_json(
            {"action":"get_messages","messages":serialized_messages}
        )
    # Chatdan barcha xabarlarni olish uchun yordamchi method
    @database_sync_to_async
    def fetch_messages(self,pk:int):
        try:
            chat = Chat.objects.get(pk=pk)
            return list(chat.messages.order_by("sent_at")) #Habarlarni sanaga ko'ra tartiblash
        except Chat.DoesNotExist:
            return []

    @database_sync_to_async
    def serialize_messages(self,messages):
        return MessageSerializer(messages,many=True,context={"user":self.user}).data

    #Bitta habarni seriyalash
    @database_sync_to_async
    def serialize_message(self,message):
        return MessageSerializer(message).data

    #Chat Obyektini olish
    @database_sync_to_async
    def get_chat(self,pk:int):
        try:
            return Chat.objects.get(pk=pk)
        except Chat.DoesNotExist:
            return None

    #Chatdagi hozirgi ishtirokchini olish
    @database_sync_to_async
    def current_users(self,chat:Chat):
        participants = ChatParticipant.objects.filter(chat=chat).select_related("user")
        return [UserSerializer(participant.user).data for participant in participants]
    #Foydalanuvchini chatdan olib tashlash
    @database_sync_to_async
    def remove_user_from_chat(self,chat_id:int):
        ChatParticipant.objects.filter(user=self.user,chat_id=chat_id).delete()

    #Foydalanuvchini chatga qo'shish
    @database_sync_to_async
    def add_user_to_chat(self,chat_id:int):
        chat = Chat.objects.get(pk=chat_id)
        if not ChatParticipant.objects.filter(user=self.user,chat=chat).exists():
            ChatParticipant.objects.create(user=self.user,chat=chat)

    #Foydalanuvchilarni seriyalash
    @database_sync_to_async
    def serialize_users(self,users):
        return UserSerializer(users,many=True).data

    #Foydalanuvchi holatini yangilash
    @database_sync_to_async
    def update_user_status(self,is_online):
        self.user.is_online = is_online
        self.user.update_last_seen() #Oxirgi ko'rilgan vaqtni yangilash
        self.user.save()
