from django.contrib import admin
from .models import DayOfWeek, Reminder, ReminderLog

admin.site.register(ReminderLog)
admin.site.register(Reminder)
admin.site.register(DayOfWeek)

