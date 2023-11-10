from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy
from crispy_forms.layout import Layout, Row, Column
from phonenumber_field.modelfields import PhoneNumberField


from django.conf import settings
from .managers import UserManager

from django.utils.translation import gettext as _
from django.contrib.gis.db.models import PointField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    
    last_known_position = PointField(verbose_name=_('dernière localisation connue'), blank=True, null=True, default=None)
    mobile_number = PhoneNumberField(_('numéro de téléphone mobile'), unique=True, null=True, default=None)
    date_joined = models.DateTimeField(_('date d\'inscription'), default=timezone.now)
    password = models.CharField(_('mot de passe'), max_length=128, blank=True)

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    list_display = ('id', 'mobile_number', 'is_active')
    list_filter = ('is_active',)
    
    layout = Layout(
        Row(
            Column('first_name'),
            Column('last_name')
        ),
        'mobile_number',
        Row(
            Column('user_permissions'),
            Column('groups')
        ),
        Row(
            Column('is_staff'),
            Column('is_active'),
            Column('is_superuser')
        )
    )

    def __str__(self):
        if not self.name: return self.mobile_number.as_e164
        return self.get_full_name()

    @property
    def name(self):
        return self.get_full_name()

    def get_absolute_url(self):
        meta = self._meta
        return reverse_lazy('core:change', kwargs={'app': meta.app_label, 'model': meta.model_name, 'pk': self.pk})