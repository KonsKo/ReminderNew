from celery import shared_task

from django.utils import timezone

from .models import Reminder, ReminderLog

now = timezone.now()
now_plus_hour = now + timezone.timedelta(hours=1)


# Process reminders with exact time, run every hour
@shared_task(name='exact_every_hour')
def exact_every_hour():
    # get 'active' reminders with exact time
    reminders_exact_time = Reminder.objects.filter(status=1).\
        filter(time_reminder__isnull=False).\
        prefetch_related()

    # get reminders between 'now' and plus one hour for processing reminder
    reminders_hour = reminders_exact_time.filter(
        time_reminder__gt=now.time(),
        time_reminder__lte=now_plus_hour.time()
    )

    # do remind
    for reminder in reminders_hour:
        ReminderLog.objects.create(
            reminder=reminder,
            status='success'
        )

# Process day reminders (with no exact time), run at 08:00 am
@shared_task(name='for_day')
def for_day():
    # get 'active' reminders with NO exact time
    reminders_no_exact_time = Reminder.objects.filter(status=1). \
        filter(time_reminder__isnull=True). \
        prefetch_related()

    # do remind
    for reminder in reminders_no_exact_time:
        ReminderLog.objects.create(
            reminder=reminder,
            status='success'
        )


# Check reminders for status, if 'date_finish' less 'now', status go to 'archived', run run at 00:01 am
@shared_task(name='check_active')
def check_active():
    # get active reminders
    reminders_active = Reminder.objects.filter(status=1).prefetch_related()

    for reminder in reminders_active:
        if reminder.date_finish < now.date():
            reminder.status = 2
            reminder.save()




