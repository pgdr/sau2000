# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime as dt

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.http import Http404
from django.utils.translation import gettext as _

from .forms import DoseForm, SheepForm

from .views_util import _get_sheep_or_404, _get_sheep

from sau.models import Farm

def _date_with_now_time(date):
    now = dt.now()
    now_hour, now_minute = now.hour, now.minute
    return date.replace(hour=now_hour, minute=now_minute, second=0)


@login_required
def _save_dose(request, slug):
    form = DoseForm(request.POST)
    if form.is_valid():
        dose_ = form.save(commit=False)
        dose_.sheep = _get_sheep_or_404(request, slug)
        dose_.date_utc = _date_with_now_time(dose_.date_utc)
        dose_.save()
    else:
        raise ValueError('Invalid form for dose: %s' % str(request.POST))


@login_required
def add_dose(request, slug=''):
    if request.method not in ('POST', 'GET'):
        raise Http404

    # on (method.POST and form.valid) we redirect to sau, else we return
    # TemplateResponse with form

    current_sheep = _get_sheep_or_404(request, slug)

    if request.method == "POST":
        form = DoseForm(request.POST)
        if form.is_valid():
            _save_dose(request, slug)
            return redirect('sau', slug=slug)
        else:
            form = DoseForm(initial={
                'sheep': current_sheep,
                'date_utc': dt.now(),
                'medicine': request.POST.get('medicine', 1)
            })

    elif request.method == "GET":
        form = DoseForm(initial={'sheep': current_sheep, 'date_utc': dt.now()})

    return TemplateResponse(
        request, 'dose.html', context={
            'form': form,
            'sheep': current_sheep
        })


def __get_farm_for_user(request):
    farms = Farm.objects.all()
    return farms[0]
    for f in farms:
        if request.user in f.farmers:
            return f
    return None


@login_required
def create_or_edit_sheep(request, slug=''):
    if request.method not in ('POST', 'GET'):
        raise Http404

    current_sheep = _get_sheep(request, slug)
    if current_sheep is None:
        return _new_sheep(request)
    else:
        return _edit_sheep(request, current_sheep)


def _save_sheep(request, form):
    new_sheep = form.save(commit=False)
    new_sheep.farm = __get_farm_for_user(request)
    new_sheep.birth_date_utc = _date_with_now_time(new_sheep.birth_date_utc)
    new_sheep.save()
    return new_sheep


def _new_sheep(request):
    if request.method == "POST":
        form = SheepForm(request.POST)
        if form.is_valid():
            sheep = _save_sheep(request, form)
            messages.success(request, 'Created %s' % sheep.name)
            return redirect('sau', slug=sheep.slug)
        # If form was not valid, it needs to be returned as-is, since it keeps
        # track of the errors.
        else:
            messages.error(request,
                           _('Form had errors, could not create new sheep.'))

    elif request.method == "GET":
        form = SheepForm()

    return TemplateResponse(request, 'sau_edit.html', context={'form': form})


def _edit_sheep(request, sheep):
    if request.method == "POST":
        form = SheepForm(request.POST, instance=sheep)
        if form.is_valid():
            s = form.save()
            return redirect('sau', slug=s.slug)
        # Form not valid, let it pass through to the context.

    elif request.method == "GET":
        form = SheepForm(instance=sheep)

    return TemplateResponse(
        request,
        'sau_edit.html',
        context={
            'form': form,
            'sheep': sheep
        })
