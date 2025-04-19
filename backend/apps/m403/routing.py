from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/results/(?P<round_id>\d+)/$', consumers.ResultsConsumer.as_asgi()),
]