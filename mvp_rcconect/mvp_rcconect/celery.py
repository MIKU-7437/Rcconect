import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'mvp_rcconect.settings')

app = Celery('mvp_rcconect')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add_every_minute': {
        'task': 'events.tasks.get_partners_events',
        'schedule': crontab(minute='*'),
    }
}
