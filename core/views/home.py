from django.utils.translation import gettext as _
from django.shortcuts import render
from .base import BaseView
from datetime import date

from django.db.models import Sum, Count
from service.models import Ride
from django import conf

class Home(BaseView):
    today = date.today()
    template = "home.html"

    def get(self, request):
        settings = conf.settings
        rides = Ride.objects.filter(
            created_at__month=self.today.month
        ).values('status').annotate(count=Count('id'), paid=Sum('paid'), cost=Sum('cost'))
        return render(request, self.template, locals())