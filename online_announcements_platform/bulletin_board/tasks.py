from celery import task
from celery.utils.log import get_task_logger
from .models import Announcement
from django.utils import timezone
from django.conf import settings

logger = get_task_logger(__name__)


@task(bind=True)
def task_announcements_hiding(self):
    announcements = Announcement.objects.filter(is_hidden=False)
    timedelta = timezone.timedelta(days=settings.MAX_DAYS_WITHOUT_ACTIVITY)
    for announcement in announcements:
        if (announcement.last_activity + timedelta) <= timezone.now().date():
            announcement.is_hidden = True
            announcement.save()
            logger.info(f'Announcement #{announcement.id} is hidden')
