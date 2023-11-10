from django.contrib.auth import get_user_model
from django.db.models import Q
from functools import reduce
from django.apps import apps
from django.db import models



class QuerySet(models.QuerySet):
    
    def all(self, **kwargs):
        return super(QuerySet, self).all()
        """
        Employee = apps.get_model('employee', model_name='employee')
        qs = super(QuerySet, self).all()
        user = kwargs.get('user', None)
        if not user: return qs

        if user.is_superuser: return qs
        if user.is_staff: return qs
        
        filters = {}
        fields = [field for field in self.model._meta.fields if field.is_relation]
        fields = [field for field in fields if field.related_model in [get_user_model(), Employee]]
        
        filters.update({field.name:user for field in fields if field.related_model == get_user_model()})
        filters.update({field.name:user.employee for field in fields if field.related_model == Employee})

        filters.update({f'{field.name}__in': [user] for field in self.model._meta.many_to_many if field.related_model == get_user_model() })
        filters.update({f'{field.name}__in': [user.employee] for field in self.model._meta.many_to_many if field.related_model == Employee and user.employee})

        filters = {key:value for key, value in filters.items() if value}
        filters = reduce(lambda q, field: q | Q(**{field: filters.get(field)}), filters.keys(), Q())

        # try to know why is showing double from here
        return qs.filter(filters).distinct().order_by('-updated_at')
        """