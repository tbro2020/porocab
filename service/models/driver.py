from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from core.models.fields import ModelSelect2Single
from django.db import models
from core.models import Base

class Driver(Base):
    vehicule = ModelSelect2Single('service.vehicule', null=True, on_delete=models.SET_NULL)
    user = ModelSelect2Single('core.user', null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(verbose_name=_('est actif'), default=False)

    list_display = ('id', 'vehicule', 'user', 'is_active')
    layout = Layout(
        Row(
            Column('vehicule'),
            Column('user')
        ),
        'is_active'
    )

    @property
    def name(self):
        return '{}/{}'.format(self.vehicule, self.user)

    class Meta:
        verbose_name = _('chauffeur')
        verbose_name_plural = _('chauffeurs')
        unique_together = ('vehicule', 'user')