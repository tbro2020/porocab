from service.consumers import Drivers, Ride
from channels.routing import URLRouter
from django.urls import path

ws_urlpatterns = URLRouter([
    path('service/drivers/<str:locality>', Drivers.as_asgi()), # To do: specify the area of the client fetched
    path('service/ride/<int:pk>', Ride.as_asgi())
])