from celery import shared_task


@shared_task(name='loop_over_reminders')
def test():
    print('test')
