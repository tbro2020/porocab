from django.shortcuts import render, redirect
from core.forms import InlineFormSetHelper
from django.contrib import messages
from .base import BaseView

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import gettext as _
from django.apps import apps

class PasswordChange(BaseView):
    inline_formset_helper = InlineFormSetHelper()

    def get(self, request):
        model = apps.get_model('core', model_name='user')
        obj = request.user
        
        form = PasswordChangeForm(obj, request.POST)
        return render(request, "registration/password_change.html", locals())
    
    def post(self, request):
        model = apps.get_model('core', model_name='user')
        obj = request.user
        
        form = PasswordChangeForm(obj, request.POST)
        if not form.is_valid():
            messages.warning(request, _('Veuillez remplir le formulaire correctement'))
            return render(request, "registration/password_change.html", locals())
        
        user = form.save()
        update_session_auth_hash(request, user)

        messages.success(request, _('Votre mot de passe a été mis à jour avec succès'))
        return redirect("core:home")