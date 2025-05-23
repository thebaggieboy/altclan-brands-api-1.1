import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import notifications  # Import your app's routing
import chats

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'altclan.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            notifications.routing.websocket_urlpatterns,
            chats.routing.websocket_urlpatterns,
        )
    ),
})