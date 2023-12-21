from functools import reduce

from django.utils.translation import gettext as _
from core.models import Menu, Approbation
from core.models import Organization
from django.urls import reverse_lazy
from django.apps import apps



def base(request):
    if not request.user.is_authenticated: return {'organization':Organization.objects.first()}
    modules = Menu.objects.all().order_by('created_at')
    
    menu = [{
        'title': module.name,
        'href': f'#{module.name}',
        'icon': f'bi-{module.icon}',
        'children': [{
            'title': child.name,
            'href': reverse_lazy('core:list', kwargs={'app': child.app_label, 'model': child.model}),
            'permission': f'{child.app_label}.view_{child.model}'
        } for child in module.children.all() if request.user.has_perm(f'{child.app_label}.view_{child.model}')]
    } for module in modules]
    
    menu.insert(0, dict({
        'title': _('Tableau de bord'),
        'href': reverse_lazy('core:home'),
        'icon': 'bi-grid-fill',
        'forced': True
    }))
    
    menu.insert(1, dict({
        'title': _('Notification'),
        'href': reverse_lazy('core:notifications'),
        'icon': 'bi-bell-fill',
        'forced': True,
        'badge': request.user.notifications.unread().count()
    }))

    menu.insert(2, dict({
        'title': _('Action requise'),
        'href': reverse_lazy('core:action-required'),
        'icon': 'bi-lightning-fill',
        'forced': True,
        'badge': action_required(request).get('action_required_count', 0)
    }))
    
    menu.insert(len(menu), dict({
        'title': _('Paramètres'),
        'href': '#',
        'icon': 'bi-gear-fill',
        'children': [item for item in [{
            'title': _('Menus'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'menu'}),
            'permission': 'core.view_menu'
        }, {
            'title': _('Modèle de document'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'template'}),
            'permission': 'core.view_template'
        }, {
            'title': _('Page'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'page'}),
            'permission': 'core.change_page'
        }, {
            'title': _('Préférences'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'preference'}),
            'permission': 'core.view_preference'
        }, {
            'title': _('Équipe'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'user'}),
            'permission': 'core.view_user'
        }, {
            'title': _('Autorisations des groupes'),
            'href': reverse_lazy('core:list', kwargs={'app': 'auth', 'model': 'group'}),
            'permission': 'auth.view_group'
        }, {
            'title': _('Organisation'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'organization'}),
            'permission': 'core.view_organization'
        }, {
            'title': _('Flux de travail'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'flow'}),
            'permission': 'core.view_flow'
        }, {
            'title': _('Job'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'job'}),
            'permission': 'core.view_job'
        }] if request.user.has_perm(item.get('permission'))]
    }))
    
    menu.append(dict({
        'title': _('Profil'),
        'href': '#',
        'icon': 'bi-person-lines-fill',
        'children': [{
            'title': _('Modifier le mot de passe'),
            'href': reverse_lazy('core:password-change')
        }, {
            'title': _('Se déconnecter'),
            'href': reverse_lazy('logout')
        }]
    }))
    return {'menus': menu, 'organization': Organization.objects.first()}

def action_required(request):
    if not request.user.is_authenticated: return {}
    return {'action_required_count': Approbation.objects.filter(user=request.user, action__isnull=True).count()}