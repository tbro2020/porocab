from django.contrib.auth.views import PasswordResetView
from core.forms import PasswordResetForm
from django.urls import path
from core.views import *


app_name = 'core'

urlpatterns = [
    path('home', Home.as_view(), name='home'),
    path('', Landing.as_view(), name='landing'),
    path('page/<str:slug>', Page.as_view(), name='page'),
    path('password/change', PasswordChange.as_view(), name='password-change'),
    path("password_reset/", PasswordResetView.as_view(form_class=PasswordResetForm), name="password_reset"),

    path('list/<str:app>/<str:model>', List.as_view(), name='list'),
    path('create/<str:app>/<str:model>', Create.as_view(), name='create'),
    path('change/<str:app>/<str:model>/<int:pk>', Change.as_view(), name='change'),
    path('delete/<str:app>/<str:model>/<int:pk>', Delete.as_view(), name='delete'),

    path('modal/list/<str:app>/<str:model>', ListModal.as_view(), name='list-modal'),
    path('modal/create/<str:app>/<str:model>', CreateModal.as_view(), name='create-modal'),
    path('modal/change/<str:app>/<str:model>/<int:pk>', ChangeModal.as_view(), name='change-modal'),
    path('modal/delete/<str:app>/<str:model>/<int:pk>', DeleteModal.as_view(), name='delete-modal'),
    
    path('action/required', ActionRequired.as_view(), name='action-required'),
    
    path('notifications', Notifications.as_view(), name='notifications'),
    path('notification/<int:pk>', Notification.as_view(), name='notification'),
    path('print/<str:app>/<str:model>/<int:pk>', Print.as_view(), name='print'),
    path('exporter/<str:app>/<str:model>', Exporter.as_view(), name='exporter'),
    
    #path('template/import/<str:app>/<str:model>', Template.as_view(), name='template'),
    #path('approve/<str:app>/<str:model>/<int:pk>', Approve.as_view(), name='approve'),
    #path('exporter/<str:app>/<str:model>', Exporter.as_view(), name='exporter'),
    #path('importer/<str:app>/<str:model>', Importer.as_view(), name='importer'),

    #path('process/<int:pk>', Process.as_view(), name='process'),
    #path('tree/<int:pk>', Tree.as_view(), name='tree'),
]
