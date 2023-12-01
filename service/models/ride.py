from api.serializers import model_serializer_factory
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
    ENDED = 'ended', _('ended')


class Ride(Base):
    driver = ModelSelect('core.user', verbose_name=_('chauffeur'), on_delete=models.SET_NULL, null=True, default=None, related_name='%(app_label)s_%(class)s_driver')
    passenger = ModelSelect('core.user', verbose_name=_('passenger'), on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_passenger')
    status = models.CharField(verbose_name=_('status'), max_length=20, default=RideStatus.PENDING, choices=RideStatus.choices)

    pick_up_address = models.CharField(_('nom du lieu de ramassage'), max_length=255)
    pick_up_location = PointField(_('lieu de ramassage'), null=True)

    duration_in_minutes = models.PositiveIntegerField(verbose_name=_('duration'), default=0)
    cost = MoneyField(max_digits=14, decimal_places=2, default=0)
    paid = MoneyField(max_digits=14, decimal_places=2, default=0)

    rating = models.PositiveIntegerField(verbose_name=_('rating'), default=0)
    review = models.TextField(verbose_name=_('review'), blank=True, null=True, default=None)

    list_display = ('id', 'passenger', 'driver', 'cost', 'paid', 'status')
    list_filter = ('status', )
    layout = Layout(
        Row(
            Column('passenger'),
            Column('driver')
        ),
        'pick_up_address',
        Row(
            Column('duration_in_minutes'),
            Column('cost'),
            Column('paid'),
        ),
        'status'
    )
    _layout = layout

    @property
    def name(self):
        return '#{} of {} on {}'.format(self.id, self.passenger, self.status)
    
    @property
    def serialized(self):
        serializer = model_serializer_factory(self._meta.model)
        return serializer(self, many=False).data

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')
        ordering = ('-updated_at', '-created_at')