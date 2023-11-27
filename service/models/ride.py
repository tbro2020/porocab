from django.contrib.gis.db.models import PointField
from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from djmoney.models.fields import MoneyField
from core.models.fields import ModelSelect
from django.db import models
from core.models import Base

class RideStatus(models.TextChoices):
    PENDING = 'pending', _('pending')
    ACCEPTED = 'accepted', _('accepted')
    STARTED = 'started', _('started')
    COMPLETED = 'completed', _('completed')
    CANCELLED = 'cancelled', _('cancelled')
    FAILED = 'failed', _('failed')


class Ride(Base):
    driver = ModelSelect('core.user', verbose_name=_('chauffeur'), on_delete=models.SET_NULL, null=True, default=None, related_name='%(app_label)s_%(class)s_driver')
    client = ModelSelect('core.user', verbose_name=_('client'), on_delete=models.SET_NULL, null=True, related_name='%(app_label)s_%(class)s_client')
    status = models.CharField(verbose_name=_('status'), max_length=20, default=RideStatus.PENDING, choices=RideStatus.choices)

    cost = MoneyField(default=0, max_digits=14, decimal_places=2, default_currency='USD')
    paid = MoneyField(default=0, max_digits=14, decimal_places=2, default_currency='USD')

    list_display = ('id', 'client', 'driver', 'cost', 'paid')
    list_filter = ('status', )
    layout = Layout(
        Row(
            Column('client'),
            Column('driver')
        ),
        #Row(
        #    Column('pick_up'),
        #    Column('drop_off'),
        #),
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
        verbose_name = _('course')
        verbose_name_plural = _('courses')