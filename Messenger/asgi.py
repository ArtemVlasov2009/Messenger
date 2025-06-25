import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
import Messenger_App.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Messenger.settings') # <-- Замените 'your_project' на имя вашего проекта

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": SessionMiddlewareStack(
        AuthMiddlewareStack(
            URLRouter(
                Messenger_App.routing.ws_urlpatterns
            )
        )
    ),
})