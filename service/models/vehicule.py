from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from django.db import models
from core.models import Base

class Vehicule(Base):
    brand = models.CharField(verbose_name=_('marque'), max_length=100)
    model = models.CharField(verbose_name=_('modèle'), max_length=100)
    color = models.CharField(verbose_name=_('couleur'), max_length=100)
    
    vin = models.CharField(verbose_name=_('numéro d\'identification du véhicule'), max_length=100, blank=True, null=True, default=None)
    license_plate= models.CharField(verbose_name=_('plaque d\'immatriculation'), max_length=100)

    list_display = ('id', 'brand', 'model', 'color', 'license_plate')
    list_filter = ('brand', 'model', 'color')
    layout = Layout(
        Row(
            Column('brand'),
            Column('model'),
            Column('color')
        ),
        Row(
            Column('license_plate'),
            Column('vin')
        )
    )
    _layout = layout

    @property
    def name(self):
        return '{}/{} with {}'.format(self.brand, self.model, self.license_plate)

    class Meta:
        verbose_name = _('véhicule')
        verbose_name_plural = _('véhicules')