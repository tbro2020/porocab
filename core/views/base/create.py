from django.utils.translation import gettext as _
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.contrib import messages

from core.forms import modelform_factory, InlineFormSetHelper
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION
from django.shortcuts import render, redirect
from crispy_forms.layout import Layout
from django.apps import apps
from .base import BaseView

from core.models import Approbation
from core.models import Flow


class Create(BaseView):
    next = None
    action = ["add"]
    template_name = "create.html"
    inline_formset_helper = InlineFormSetHelper()
    
    def get(self, request, app, model):
        model = apps.get_model(app, model_name=model)
        
        fields = getattr(model, 'layout', '__all__')
        fields = [field.name for field in fields.get_field_names()] if isinstance(fields, Layout) else fields

        form = modelform_factory(model, fields=fields)
        form = form()
        
        formsets = [apps.get_model(inline.split('.')[0], model_name=inline.split('.')[-1]) for inline in getattr(model, 'inlines', [])]
        formsets = [inlineformset_factory(model, inline, fields=getattr(inline, 'inline_form_fields', '__all__'), can_delete=False, extra=1) for inline in formsets]
        
        return render(request, self.template_name, locals())
    
    def post(self, request, app, model):
        model = apps.get_model(app, model)

        fields = getattr(model, 'layout', '__all__')
        fields = [field.name for field in fields.get_field_names()] if isinstance(fields, Layout) else fields
        
        form = modelform_factory(model, fields=fields)
        form = form(request.POST or None, request.FILES or None)

        formsets = [apps.get_model(inline.split('.')[0], model_name=inline.split('.')[-1]) for inline in getattr(model, 'inlines', [])]
        formsets = [inlineformset_factory(model, inline, fields=getattr(inline, 'inline_form_fields', '__all__'), can_delete=False, extra=1) for inline in formsets]
        formsets = [formset(request.POST or None, request.FILES or None) for formset in formsets]

        if not form.is_valid() or False in [formset.is_valid() for formset in formsets]:
            [messages.error(request, str(error)) for error in form.errors]
            return render(request, self.template_name, locals())
        form.save()

        # Add approvers
        flow = Flow.objects.filter(content_type__model=model._meta.model_name).first()
        flow = flow.steps.values_list('user', flat=True).distinct() if flow else []
        if approvers := form.cleaned_data.get('approvers', flow):
            approvers = [Approbation(
                content_type=ContentType.objects.get_for_model(model), 
                object_id=form.instance.id, 
                user_id=getattr(approver, 'id', approver)) for approver in approvers
            ]
            Approbation.objects.bulk_create(approvers)

        for formset in formsets:
            qs = formset.save(commit=False)
            for obj in qs:
                setattr(obj, formset.fk.name, form.instance)
                obj.save()

        self.log(model, form, action=ADDITION, formsets=formsets)
        self.notify_approvers(model, form.instance)
        
        messages.add_message(request, messages.SUCCESS, message=_('Le {model} a été créé avec succès').format(**{'model': model._meta.model_name}))
        next = request.GET.dict().get('next', reverse_lazy('core:list', kwargs={'app': app, 'model': model._meta.model_name}))
        return self.next if self.next else redirect(next)