from celery import shared_task

from django.utils import timezone

from .models import Reminder, ReminderLog


@shared_task(name='do_remind')
def do_reminde():
    now = timezone.now().date()
    active_reminders_status = Reminder.objects.filter(status=1)

    active_reminders = active_reminders_status.filter(date_start__lte=now).filter(date_finish__gt=now)
    
    for active_reminder in active_reminders:
        ReminderLog.objects.create(
            reminder=active_reminder,
            status='success'
        )
        
        



