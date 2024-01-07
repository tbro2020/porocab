from service.consumers import RideConsumer, Drivers
from channels.routing import URLRouter
from django.urls import path

ws_urlpatterns = URLRouter([
    path('service/ride/<int:pk>', RideConsumer.as_asgi()),
    path('drivers', Drivers.as_asgi()),
])