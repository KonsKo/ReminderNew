from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, PopRequestMixin, CreateUpdateAjaxMixin

from .models import Reminder


class CreateRemForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Reminder
        exclude = ['user', 'status',]

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



