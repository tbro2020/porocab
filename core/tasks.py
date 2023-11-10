from datetime import datetime
from celery import shared_task
from django.apps import apps

@shared_task(name='daily')
def daily():
    qs = apps.get_model('core', 'job').objects.all()
    for obj in qs:
        try:
            print(obj.name, datetime.now())
            eval(obj.job, locals())
        except:
            pass
