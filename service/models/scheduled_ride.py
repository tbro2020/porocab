from core.models.fields import ModelSelect, TimeField
from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from djmoney.models.fields import MoneyField

from django.db import models
from core.models import Base

class RideChoices(models.TextChoices):
    CREATED = 'CREATED', 'CREATED'

class ScheduledRide(Base):
    driver = ModelSelect('core.user', verbose_name=_('chauffeur'), on_delete=models.SET_NULL, null=True, default=None, related_name='%(app_label)s_%(class)s_client')
    client = ModelSelect('core.user', verbose_name=_('client'), on_delete=models.SET_NULL, null=True, default=None, related_name='%(app_label)s_%(class)s_driver')

    drop_off = models.CharField(verbose_name=_('drop off'), max_length=100)
    pick_up = models.CharField(verbose_name=_('pick up'), max_length=100)
    
    pick_up_time = TimeField(verbose_name=_('heure de prise en charge'))

    cost = MoneyField(default=0, max_digits=14, decimal_places=2, default_currency='USD')
    paid = MoneyField(default=0, max_digits=14, decimal_places=2, default_currency='USD')

    status = models.CharField(verbose_name=_('status'), max_length=10, default='CREATED', choices=RideChoices.choices)

    list_display = ('id', 'client', 'driver', 'cost', 'paid')
    list_filter = ('status', )
    layout = Layout(
        Row(
            Column('client'),
            Column('driver')
        ),
        Row(
            Column('pick_up'),
            Column('drop_off'),
        ),
        Row(
            Column('cost'),
            Column('paid'),
        ),
        'status'
    )
    _layout = layout

    def name(self):
        return '#{} of {} on {}'.format(self.id, self.client, self.status)

    class Meta:
        verbose_name = _('course programmée')
        verbose_name_plural = _('courses programmée')