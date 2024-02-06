from django.contrib.gis.db.models import PointField
from django.utils.translation import gettext as _
from djmoney.models.fields import MoneyField
from crispy_forms.layout import Layout

from django.db import models
from core.models import Base

class Invoice(Base):
    pick_up_location = PointField(_('lieu de ramassage'), null=True, blank=True, editable=False)
    pick_up_address = models.CharField(_('nom du lieu de ramassage'), max_length=255)

    duration_in_minutes = models.PositiveIntegerField(_('duree en minute'), null=True, blank=True)
    price = MoneyField(_('prix'), max_digits=14, decimal_places=2, default=0.0)

    @property
    def name(self):
        return f'{self.pk}'
    
    list_display = ('id', 'duration_in_minutes', 'pick_up_location_name', 'price')
    layout = Layout('duration_in_minutes', 'pick_up_location_name')

    class Meta:
        verbose_name = _('pro-forma')
        verbose_name_plural = _('pro-formas')
