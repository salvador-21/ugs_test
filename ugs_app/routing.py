from django.urls import path
from .consumers import WSArena

ws_urlpatterns =[
    path('ws/arena/<str:game_id>',WSArena.as_asgi())
]