from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.contrib import messages
from django.urls import reverse
from django.http import Http404
from django.apps import apps

from django.contrib.contenttypes.models import ContentType
from core.views import BaseView


class Approbation(BaseView):
    action = ["change"]

    def get(self, request, action, app, model, pk):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, pk=pk)
        return render(request, "approve.html", locals())

    def post(self, request, action, app, model, pk):
        model = apps.get_model(app, model)
        obj = get_object_or_404(model, id=pk)
        approbations = self.approbations()
        
        if request.user.id not in approbations.users():
            messages.warning(request, _('Vous n\'êtes pas désigné comme approbateur'))
            return redirect(obj.get_absolute_url())
        
        # To-Do: Review this code
        #if approbation.filter(user=request.user.pk,).exists():
        #    messages.warning(request, _('You have already approved'))
        #    return redirect(reverse('core:change', kwargs={'app': app, 'model': model._meta.model_name, 'pk': obj.pk}))
        
        # To-Do: Review this code to not allow all user to approve
        if action.upper() not in ['APPROVED', 'REJECTED']: raise Http404
        approbation = approbations.filter(user=request.user).update(action=action.upper())
        messages.success(request, _('Vous avez approuvé le {model} #{id}').format(model=model._meta.verbose_name, id=obj.pk))

        #obj = self.approvers_from_process(model, obj)
        #notified_on_approved(model._meta.app_label, model._meta.model_name, obj.pk, False)

        next = request.GET.get('next', obj.get_absolute_url())
        return redirect(next)