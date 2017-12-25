# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime as dt

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.http import Http404

from .forms import DoseForm, SheepForm

from .views_util import _get_sheep_or_404

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


@login_required
def _save_sheep(request, slug):
    form = SheepForm(request.POST)
    if form.is_valid():
        new_sheep = form.save(commit=False)
        sheep = _get_sheep_or_404(request, slug)
        sheep.name = new_sheep.name
        sheep.ear_tag = new_sheep.ear_tag
        sheep.ear_tag_color = new_sheep.ear_tag_color
        sheep.birth_date_utc = _date_with_now_time(new_sheep.birth_date_utc)
        sheep.sex = new_sheep.sex
        sheep.mother = new_sheep.mother
        sheep.father = new_sheep.father
        sheep.origin = new_sheep.origin
        sheep.save()
    else:
        raise ValueError('Invalid form for sheep: %s' % str(request.POST))


@login_required
def edit_sheep(request, slug=''):
    if request.method not in ('POST', 'GET'):
        raise Http404

    current_sheep = _get_sheep_or_404(request, slug)

    if request.method == "POST":
        form = SheepForm(request.POST)
        if form.is_valid():
            _save_sheep(request, slug)
            return redirect('sau', slug=slug)
        else:
            form = SheepForm(instance=current_sheep)

    elif request.method == "GET":
        form = SheepForm(instance=current_sheep)

    return TemplateResponse(
        request,
        'sau_edit.html',
        context={
            'form': form,
            'sheep': current_sheep
        })


@login_required
def __get_farm_for_user(request):
    farms = Farm.objects.all()
    return farms[0]
    for f in farms:
        if request.user in f.farmers:
            return f
    return None


@login_required
def _create_sheep(request):
    form = SheepForm(request.POST)
    if form.is_valid():
        new_sheep = form.save(commit=False)
        new_sheep.farm = __get_farm_for_user(request)
        new_sheep.birth_date_utc = _date_with_now_time(new_sheep.birth_date_utc)
        new_sheep.save()
        return new_sheep.slug
    else:
        raise ValueError('Invalid form for sheep: %s' % str(request.POST))



def __sheep_form_values(request):
    def GET(k, default=''):
        return request.POST.get(k, default)

    return {
        'name': GET('name'),
        'ear_tag': GET('ear_tag'),
        'ear_color': GET('ear_tag_color', 'w'),
        'birth_date_utc': GET('birth_date_utc', dt.now()),
        'sex': GET('sex', 'f'),
        'mother': GET('mother', None),
        'father': GET('father', None),
        'origin': GET('origin'),
    }

@login_required
def new_sheep(request):
    if request.method not in ('POST', 'GET'):
        raise Http404

    if request.method == "POST":
        form = SheepForm(request.POST)
        if form.is_valid():
            slug = _create_sheep(request)
            return redirect('sau', slug=slug)
        else:
            # likely missing required field
            # form.errors is an HTML string of error fields
            form = SheepForm(initial=__sheep_form_values(request))

    elif request.method == "GET":
        form = SheepForm()

    return TemplateResponse(request, 'new_sheep.html', context={'form': form})
