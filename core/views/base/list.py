from core.filters import filter_set_factory
from django.core.paginator import Paginator
from django.shortcuts import render
from django.apps import apps
from .base import BaseView


class List(BaseView):
    qs = None
    action = ["view"]
    template_name = "list.html"

    def get(self, request, app, model):
        model = apps.get_model(app, model_name=model)
        list_filter = getattr(model, 'list_filter', [])
        list_display = [field for field in model._meta.fields if field.name in getattr(model, 'list_display', [])]
        
        self.qs = model.objects.select_related().prefetch_related()#.order_by('-created_at')
        try:
            self.qs = self.qs.all(user=request.user)
        except Exception:
            self.qs = self.qs.all()
        
        # Hard filter
        query = {k:v for k, v in request.GET.dict().items() if v}
        fields = [field.name for field in model._meta.fields if field.name]
        self.qs = self.qs.filter(**{k:v for k, v in query.items() if k.split("__")[0] in fields})

        # Soft filter
        qs_filter = filter_set_factory(model, fields=list_filter)
        qs_filter = qs_filter(request.GET, queryset=self.qs)
        self.qs = qs_filter.qs.order_by('-id')
        
        paginator = Paginator(self.qs, 25)
        self.qs = paginator.page(int(request.GET.dict().get('page', 1)))
        return render(request, getattr(model, "change_list_template", self.template_name), locals())