import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_announcements_platform.settings')

app = Celery('online_announcements_platform')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-orders-every-day': {
        'task': 'bulletin_board.tasks.task_announcements_hiding',
        'schedule': crontab(hour=0, minute=0),
    }
}