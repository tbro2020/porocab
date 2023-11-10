from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.shortcuts import render
from django.db.models import Count
from .base import BaseView

from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.apps import apps
from datetime import date



class Home(BaseView):
    today = date.today()

    def get(self, request):
        return render(request, "home.html", locals())