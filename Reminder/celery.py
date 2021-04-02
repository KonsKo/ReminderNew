import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Reminder.settings')

BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

app = Celery('Reminder')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_url = BASE_REDIS_URL

app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'

app.conf.beat_schedule = {
    'reminder1': {
        'task': 'exact_every_hour',
        'schedule': crontab(
            minute='*',
            hour='*',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*'
        ),
    },
    'reminder2': {
        'task': 'for_day',
        'schedule': crontab(
            minute='0',
            hour='8',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*'
        ),
    },
    'reminder3': {
        'task': 'check_active',
        'schedule': crontab(
            minute='1',
            hour='0',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*'
        ),
    },
}


