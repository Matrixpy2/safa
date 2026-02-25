"""
ASGI config for safa project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safa.settings')

# application = get_asgi_application()

# # change application to routing.py
# from channels.routing import ProtocolTypeRouter , URLRouter
# from channels.auth import AuthMiddlewareStack
# from chat_app.routing import websocket_urlpatterns as chat_websocket_urlpatterns

# application = ProtocolTypeRouter(
#     {
#         'http' : get_asgi_application(),
#         'websocket' : AuthMiddlewareStack(
#             URLRouter(
#                 chat_websocket_urlpatterns
#             )
#         )
#     }
# )
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack 
from chat_app.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

