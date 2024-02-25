from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy
from crispy_forms.layout import Layout, Row, Column
from phonenumber_field.modelfields import PhoneNumberField


from django.conf import settings
from .managers import UserManager

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

class User(AbstractUser):
    date_joined = models.DateTimeField(_('date d\'inscription'), default=timezone.now)
    proof_of_id = models.FileField('preuve d\'identité', upload_to='proof_of_id/')
    mobile_number = PhoneNumberField(_('numéro de téléphone mobile'), unique=True)
    password = models.CharField(_('mot de passe'), max_length=128)

    USERNAME_FIELD, REQUIRED_FIELDS = 'mobile_number', []
    username, email = None, None

    objects = UserManager()
    
    list_display = ('id', 'mobile_number', 'is_active', 'created_at')
    list_filter = ('is_active',)
    
    layout = Layout(
        Row(
            Column('proof_of_id', css_class='form-group col-md-4'),
            Column('first_name', css_class='form-group col-md-4'),
            Column('last_name', css_class='form-group col-md-4')
        ),
        'mobile_number',
        Row(
            Column('user_permissions', css_class='form-group col-md-6'),
            Column('groups', css_class='form-group col-md-6')
        ),
        Row(
            Column('is_superuser', css_class='form-group col-md-4'),
            Column('is_active', css_class='form-group col-md-4'),
            Column('is_staff', css_class='form-group col-md-4')
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