from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from core.models.fields import ModelSelect
from django.db import models
from core.models import Base

class Vehicle(Base):
    driver = ModelSelect('core.user', verbose_name=_('chauffeur'), on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_driver')

    brand = models.CharField(verbose_name=_('marque'), max_length=100)
    model = models.CharField(verbose_name=_('modèle'), max_length=100)
    color = models.CharField(verbose_name=_('couleur'), max_length=100)
    
    vin = models.CharField(verbose_name=_('numéro d\'identification du véhicule'), max_length=100, blank=True, null=True, default=None)
    licence= models.CharField(verbose_name=_('plaque d\'immatriculation'), max_length=100)

    list_display = ('id', 'driver', 'brand', 'model', 'color', 'licence', 'vin')
    list_filter = ('brand', 'model', 'color')
    layout = Layout(
        'driver',
        Row(
            Column('brand'),
            Column('model'),
            Column('color')
        ),
        Row(
            Column('licence'),
            Column('vin')
        )
    )
    _layout = layout

    @property
    def name(self):
        return '{}/{} with {}'.format(self.brand, self.model, self.licence)

    class Meta:
        verbose_name = _('véhicule')
        verbose_name_plural = _('véhicules')