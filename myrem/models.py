from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DayOfWeek(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Reminder(models.Model):
    STATUS = (
        (1, 'Active'),
        (2, 'Archived'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = models.CharField(max_length=256)
    date_create = models.DateTimeField(auto_now_add=True)
    date_start = models.DateField()
    date_finish = models.DateField()
    time_reminder = models.TimeField()
    day_of_week = models.ManyToManyField(DayOfWeek)
    status = models.IntegerField(choices=STATUS, default=1)

    def __str__(self):
        return self.title


class ReminderLog(models.Model):
    STATUS=(
        ('s', 'success'),
        ('f', 'fail'),
    )

    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)

    def __str__(self):
        return r'{},{},{}'.format(self.reminder.title, self.date, self.status)

