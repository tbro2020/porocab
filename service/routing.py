from service.consumers import Drivers, Ride
from channels.routing import URLRouter
from django.urls import path

ws_urlpatterns = URLRouter([
    path('service/drivers', Drivers.as_asgi()),
    path('service/ride/<int:pk>', Ride.as_asgi())
])