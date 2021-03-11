from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Reminder, DayOfWeek

import datetime

class ReminderTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user1', password='123123')

        self.monday = DayOfWeek.objects.create(name='Monday')
        self.saturday = DayOfWeek.objects.create(name='Sarurday')

        self.time = datetime.datetime.strptime('9:00', '%H:%M')

        self.reminder1 = Reminder.objects.create(
            user=self.user,
            title='title1',
            text='text1',
            date_start=datetime.datetime.strptime('20 Sep 2030', '%d %b %Y'),
            date_finish=datetime.datetime.strptime('25 Sep 2030', '%d %b %Y'),
            time_reminder=self.time,
        )
        self.reminder1.day_of_week.add(self.monday.id)
        self.reminder1.day_of_week.add(self.saturday.id)
        self.reminder1.save()

    def test_Model_create_rem_start_lt_finish(self):
        reminder2 = Reminder.objects.create(
            user=self.user,
            title='title2',
            text='text2',
            date_start=datetime.datetime.strptime('20 Sep 2030', '%d %b %Y'),
            date_finish=datetime.datetime.strptime('19 Sep 2030', '%d %b %Y'),
            time_reminder=self.time
        )
        try:
            reminder2.full_clean()
        except ValidationError as err:
            self.assertEqual(err.messages[0], 'Date finish has to be grater date start.')

    def test_Model_create_rem_start_and_finish_gt_now(self):
        reminder2 = Reminder.objects.create(
            user=self.user,
            title='title2',
            text='text2',
            date_start=datetime.datetime.strptime('18 Sep 2020', '%d %b %Y'),
            date_finish=datetime.datetime.strptime('19 Sep 2020', '%d %b %Y'),
            time_reminder=self.time
        )
        try:
            reminder2.full_clean()
        except ValidationError as err:
            self.assertEqual(err.messages[0], 'Date finish has to be grater current date.')

    '''def test_Model_test_create_rem_start_gt_now(self):
        reminder3 = Reminder.objects.create(
            user=self.user,
            title='title2',
            text='text2',
            date_start=datetime.datetime.strptime('18 Sep 2020', '%d %b %Y'),
            date_finish=datetime.datetime.strptime('19 Sep 2021', '%d %b %Y'),
            time_reminder=self.time
        )

        try:
            reminder3.full_clean()
        except ValidationError as err:
            self.assertEqual(err.messages[0], 'Creating: Date finish and date start has to be grater current date.')'''
