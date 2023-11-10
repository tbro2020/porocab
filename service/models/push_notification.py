from crispy_forms.layout import Layout, Row, Column
from core.models.fields import ModelSelect2Multiple
from django.utils.translation import gettext as _
from core.utils import upload_directory_file
from django.db import models
from core.models import Base

class TypeOfUserChoice(models.TextChoices):
    EMPTY = '-', ''
    CLIENT = 'client', _('client')
    DRIVER = 'driver', _('chauffeur')

class PushNotification(Base):
    title = models.CharField(verbose_name=_('titre'), max_length=100)
    description = models.TextField(verbose_name=_('description'))

    users = ModelSelect2Multiple('core.user', verbose_name=_('utilisateurs'))
    attach = models.ImageField(verbose_name=_('joindre'), upload_to=upload_directory_file, blank=True, null=True, default=None)
    type_of_user = models.CharField(verbose_name=_('type d\'utilisateur'), max_length=10, blank=True, null=True, default=None, choices=TypeOfUserChoice.choices)

    list_display = ('id', 'title', 'type_of_user')
    list_filter = ('type_of_user',)

    layout = Layout(
        'approvers',
        'title',
        'description',
        'attach',
        Row(
            Column('type_of_user'),
            Column('users')
        )
    )

    _layout = Layout(
        'title',
        'description',
        'attach',
        Row(
            Column('type_of_user'),
            Column('users')
        )
    )
    

    class Meta:
        verbose_name = _('notification push')
        verbose_name_plural = _('notifications push')