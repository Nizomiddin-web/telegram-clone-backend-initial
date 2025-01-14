import os

import django
import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.db import close_old_connections

from channels.sessions import CookieMiddleware,SessionMiddleware
from rest_framework_simplejwt.utils import aware_utcnow

from user.models import User

ALGORITHM = "HS256"

#Django settings yuklash
os.environ.setdefault("DJANGO_SETTINGS_MODULE","config.settings")
django.setup()

#Foydalanuvchini jwt token orqali olish funksiyasi
@database_sync_to_async
def get_user(token):
    try:
        #Tokenni decode qilish
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        #Token muddati tugagan bo'lsa
        return AnonymousUser()
    except jwt.InvalidTokenError:
        #token yaroqsiz bo'lsa
        return AnonymousUser()
    try:
        user = User.objects.get(id=payload['user_id'])
    except User.DoesNotExist:
        #Foydalanuvchi mavjud emas
        return AnonymousUser()
    return user

# JWT authentifikatsiya Middleware
class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope,receive,send):
        close_old_connections()
        token_key = None
        query_string = scope.get("query_string",b"").decode()

        #Queary string orqali tokkeni olish
        if query_string:
            token_key = dict(x.split("=") for x in query_string.split("&")).get('token')
        #Foydalanuvchi aniqlash va scope'ga qo'shish
        scope['user']  = await get_user(token_key)
        return await super().__call__(scope,receive,send)

#WebSocket Uchun middleware Stack
def JWTAuthMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(TokenAuthMiddleware(inner)))