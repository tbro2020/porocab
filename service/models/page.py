from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from tinymce.models import HTMLField
from autoslug import AutoSlugField
from django.db import models
from core.models import Base


class Page(Base):
    url = models.URLField(verbose_name=_('url'), null=True, blank=True)
    title = models.CharField(verbose_name=_('titre'),max_length=255)
    content = HTMLField(verbose_name=_('contenu'), null=True)
    slug = AutoSlugField(populate_from='title')
    
    @property
    def name(self):
        return self.title

    list_display = ('id', 'title', 'slug', 'url', 'created_at', 'updated_at')
    layout = Layout('title', 'content')

    def save(self, *args, **kwargs):
        self.url = 'https://www.google.com/search?q={}'.format(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')