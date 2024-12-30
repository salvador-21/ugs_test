import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from ugs_app.routing import ws_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ugs_proj.settings')

# application = get_asgi_application()
application=ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(ws_urlpatterns))
    )
    
})
