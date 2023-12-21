from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _

from django.template import Context, Template
from django.views import View
from django.apps import apps

class Page(View):
    action = ["view"]

    def get(self, request, slug):
        app, model = 'core', 'page'
        self.kwargs.update({'app': app, 'model': model})

        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, slug=slug)

        template = Template(obj.content)
        context = Context(vars(obj))
        context['obj'] = obj

        template = template.render(context)
        return render(request, 'page.html', locals())
