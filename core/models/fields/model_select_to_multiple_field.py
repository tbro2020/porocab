from django.urls import reverse_lazy
from django.db import models
from dal import autocomplete


class ModelSelect2Multiple(models.ManyToManyField):
    def formfield(self, **kwargs):
        kwargs['widget'] = autocomplete.ModelSelect2Multiple(url=reverse_lazy('api:autocomplete', kwargs={
            'to_field': 'pk',
            'app': self.remote_field.model._meta.app_label,
            'model': self.remote_field.model._meta.model_name
        }))
        return super().formfield(**kwargs)