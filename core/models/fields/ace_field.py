from django_ace import AceWidget
from django.db import models


class AceField(models.TextField):
    def formfield(self, **kwargs):
        kwargs['widget'] = AceWidget(mode='python', theme='dracula', width='100% !important', toolbar=False, showgutter=False)
        return super().formfield(**kwargs)