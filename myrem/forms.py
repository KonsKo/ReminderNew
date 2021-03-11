from django import forms
from django.core.exceptions import ValidationError

from bootstrap_modal_forms.forms import BSModalModelForm, PopRequestMixin, CreateUpdateAjaxMixin

import datetime

from .models import Reminder


class CreateRemForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Reminder
        exclude = ['user', 'status',]

    '''def clean(self):
        super(CreateRemForm, self).clean()
        start = self.cleaned_data['date_start']
        finish = self.cleaned_data['date_finish']
        now = datetime.datetime.now().date()
        if start < now or finish < now:
            raise ValidationError('Both dates have to be grater current date.')'''

    def save(self, commit=False):
        if not self.request.is_ajax():
            instance = super(CreateUpdateAjaxMixin, self).save(commit=commit)
            instance.user = self.request.user
            instance.save()
            for d in self.cleaned_data['day_of_week']:
                instance.day_of_week.add(d.id)
            instance.save()
        else:
            instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
        return instance


class RemModelForm(BSModalModelForm):
    class Meta:
        model = Reminder
        exclude = ['user', 'date_create',]



