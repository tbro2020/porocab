from .base import Base
from django.db import models
from tinymce.models import HTMLField
from .fields import ModelSelect2Single
from django.utils.translation import gettext as _
from crispy_forms.layout import Layout, Row, Column
from django.contrib.contenttypes.models import ContentType


class Template(Base):
    content = HTMLField(_('contenu'), null=True, default=None)
    name = models.CharField(_('nom'), max_length=100, unique=True)
    content_type = ModelSelect2Single(ContentType, verbose_name=_('type de contenu'), on_delete=models.CASCADE)
    
    search_field = ('name')
    list_display = ('id', 'content_type', 'name')
    layout = Layout(Row(Column('content_type'), Column('name')), 'content')

    class Meta:
        verbose_name = _('modèle de document')
        verbose_name_plural = _('modèles de documents')