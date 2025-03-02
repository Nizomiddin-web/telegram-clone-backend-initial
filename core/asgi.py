import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from core import routing
from share.middleware import JwtAuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


application = ProtocolTypeRouter({
    "http":get_asgi_application(),
    "websocket":JwtAuthMiddlewareStack(
        URLRouter(routing.websocket_urlpatterns)
    )
})
