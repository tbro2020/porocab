from django.shortcuts import render
from django.views import View

from core import models


class Landing(View):
    def get(self, request):
        pages = models.Page.objects.filter(authentication_required=False)
        return render(request, 'landing.html', locals())