from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.views import View

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry

from django.utils.encoding import force_str
from notifications.signals import notify
from core.models import Approbation
from django.apps import apps

class BaseView(LoginRequiredMixin, PermissionRequiredMixin, View):
    def get_permission_required(self):
        data = self.kwargs
        if 'app' not in data or 'model' not in data: return []
        return [f"{data.get('app')}.{i}_{data.get('model')}" for i in self.action]
    
    def approbations(self):
        model = apps.get_model(self.kwargs.get('app'), model_name=self.kwargs.get('model'))
        return Approbation.objects.for_model(model).filter(object_id=self.kwargs.get('pk'))
    
    def activities(self):
        pk = self.kwargs.get('pk')
        app = self.kwargs.get('app')
        model = self.kwargs.get('model')
        model = apps.get_model(app, model_name=model)
        content_type = ContentType.objects.get_for_model(model)
        return LogEntry.objects.filter(**{'content_type_id': content_type.id, 'object_id': pk})
    
    def log(self, model, form, action, formsets=None):
        log_messages = []
        LogEntry.objects.log_action(
            user_id=self.request.user.id,
            content_type_id=ContentType.objects.get_for_model(model).id,
            object_id=form.instance.pk,
            object_repr=force_str(form.instance),
            action_flag=action,
            change_message=''.join(log_messages)
        )

    def notify_approvers(self, model, obj):
        approbations = self.approbations()
        if not approbations.exists(): return
        [notify.send(**{
            'sender': obj,
            'actor': self.request.user,
            'recipient': approver,
            'verb': _('Demande d\'approbation pour le/la {model} #{pk}').format(**{'model': model._meta.verbose_name, 'pk': obj.pk}),
            'action_object': obj,
            'target': obj,
            'level': 'info',
            'description': _('{user} demande votre approbation pour {model} #{pk}').format(**{'user': self.request.user, 'model': model._meta.verbose_name, 'pk': obj.pk}),
            'public': False
        }) for approver in approbations.pending().users()]