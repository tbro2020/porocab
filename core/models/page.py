from django.utils.translation import gettext as _
from crispy_forms.layout import Layout, Row, Column
from tinymce.models import HTMLField
from autoslug import AutoSlugField
from django.db import models
from core.models import Base


class Page(Base):
    short_description = models.CharField(_('description courte'), max_length=250, null=True, default=None)
    authentication_required = models.BooleanField(_('authentification requise'), default=False)

    title = models.CharField(_('titre'), max_length=100, unique=True)
    content = HTMLField(_('contenu'), null=True, default=None)
    slug = AutoSlugField(populate_from='title')

    layout = Layout(
        Row(
            Column('title', css_class='col-12 col-md-6'),
            Column('short_description', css_class='col-12 col-md-6'),
            css_class='row'
        ),
        Row(
            Column('content', css_class='col-12'),
            css_class='row'
        ),
        'authentication_required'
    )
    list_display = ('id', 'title', 'created_by')

    @property
    def name(self):
        return self.title

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')