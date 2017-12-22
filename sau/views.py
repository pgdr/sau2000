# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime as dt

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from sau.models import Sheep, Dose, Farm
from .forms import DoseForm


SAUS = [
    {
        'name': 'britanna',
        'birth_date_utc': dt.now(),
        'sex': 'f',
    },
    {
        'name': 'lolcakes',
        'birth_date_utc': dt.now(),
        'sex': 'f',
        'ear_tag': '2608',
        'ear_tag_color': 'r',
        'quality': 'e+',
    },
    {
        'name': 'rambo',
        'birth_date_utc': dt.now(),
        'sex': 'm',
        'quality': 'p-',
    },
]


def __init():
    f = Farm.objects.all()[0]
    f.save()
    for sau in SAUS:
        s = Sheep.objects.create(**sau, farm=f)
        s.save()


def get_all_sheep(request):
    if request.user.is_superuser:
        a = Sheep.objects.all()
        if len(a) == 0:
            __init()
            a = Sheep.objects.all()
        return a
    return Sheep.objects.all().filter(farm__farmers__in=[request.user])


@login_required
def index(request):
    sheep = get_all_sheep(request)
    return TemplateResponse(request, 'index.html', context={'sheep': sheep})

def _get_sheep_or_404(request, slug):
    if request.user.is_superuser:
        return get_object_or_404(Sheep, slug=slug)

    return get_object_or_404(Sheep, slug=slug,
                             farm__farmers__in=[request.user])

@login_required
def sau(request, slug=""):
    sheep = _get_sheep_or_404(request, slug)
    doses = Dose.get(sheep=sheep)
    return TemplateResponse(request, 'sau.html', context={'sheep': sheep,
                                                          'doses': doses})


@login_required
def _do_the_post(request, slug):
    form = DoseForm(request.POST)
    if form.is_valid():
        dose = form.save(commit=False)
        dose.sheep = _get_sheep_or_404(request, slug)
        h,m = dt.now().hour, dt.now().minute
        dose.date_utc = dose.date_utc.replace(hour=h, minute=m, second=0)
        dose.save()
    return redirect('sau', slug=slug)


@login_required
def dose(request, slug=''):
    if request.method == "POST":
        return _do_the_post(request, slug)
    sheep = _get_sheep_or_404(request, slug)
    form = DoseForm(initial={'sheep': sheep,
                             'date_utc': dt.now()})
    return TemplateResponse(request,
                            'dose.html',
                            context={'form': form, 'sheep': sheep})
