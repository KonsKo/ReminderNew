from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView

import datetime

from .forms import CreateRemForm, RemModelForm
from .models import Reminder


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'myrem/home_new.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        now = datetime.datetime.now()
        kwargs['rem_list_active'] = Reminder.objects.filter(user=user).filter(status=1)
        kwargs['rem_list_archive'] = Reminder.objects.filter(user=user).filter(status=2)
        return kwargs


@method_decorator(login_required, name='dispatch')
class CreateRemView(BSModalCreateView):
    template_name = 'myrem/create_rem.html'
    form_class = CreateRemForm
    success_url = reverse_lazy('home')
    success_message = 'Success: reminder has been created!'
    model = Reminder


def change_status(request):
    change = {'to_archive': 2, 'to_active': 1}
    reminder = Reminder.objects.get(id=request.GET.get('rem_id'))
    reminder.status = change.get(request.GET.get('action'))
    reminder.save()
    return render(request, 'myrem/home_new.html')


class UpdateRemView(BSModalUpdateView):
    model = Reminder
    template_name = 'myrem/update_rem.html'
    form_class = RemModelForm
    success_url = reverse_lazy('home')
    success_message = 'Success: reminder has been updated!'
