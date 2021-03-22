from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone


User = get_user_model()

class DayOfWeek(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Reminder(models.Model):
    STATUS = (
        (1, 'Active'),
        (2, 'Archived'),
        (3, 'Deleted'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, blank=False)
    text = models.CharField(max_length=256)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Reminder was created")
    date_start = models.DateField()
    date_finish = models.DateField()
    time_reminder = models.TimeField()
    day_of_week = models.ManyToManyField(DayOfWeek)
    status = models.IntegerField(choices=STATUS, default=1)

    def __str__(self):
        return r'{} --> {}'.format(self.title, dict(self.STATUS).get(self.status))

    # Method that I used for studying purpose, I do not use anymore but leave here
    # @classmethod
    # def from_db(cls, db, field_names, values):
    #     instance = super().from_db(db, field_names, values)
    #     instance._loaded_values = dict(zip(field_names, values))
    #     return instance

    def clean(self):
        super(Reminder, self).clean()
        if self.pk:
            old_status = Reminder.objects.get(pk=self.pk).status
        new_status = self.status
        start = self.date_start
        finish = self.date_finish
        now = timezone.now().date()

        # Target that I followed for this checks is understand method above
        # (there are extra unnecessary conditions for real project)
        # If we always will check date start: it is inconvenient while updating active reminder

        # Always check that date start before date finish
        if finish < start:
            raise ValidationError('Date finish has to be grater date start.')

        # Always check that date finish after current date
        # We suppose if we want to change archived reminder we want always change date,
        # if not we should change our logic
        if finish < now:
            raise ValidationError('Date finish has to be grater current date.')

        # When we are creating new Reminder, extra check that date start after current date either
        if self._state.adding:
            if start < now:
                raise ValidationError('Creating: Date finish and date start has to be grater current date.')

        # If we are updating Reminder from Archived to Active than Date start has to be grater current date,
        elif not self._state.adding:
            if old_status == 2 and new_status == 1:
                if start < now:
                    raise ValidationError('Updating: Date start has to be grater current date.')


class ReminderLog(models.Model):
    STATUS = (
        ('success', 'success'),
        ('fail', 'fail'),
    )
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)

    def __str__(self):
        return r'{}, {}, {}'.format(self.reminder.title, self.date, self.status)

