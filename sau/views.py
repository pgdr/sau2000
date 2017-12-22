# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from sau.models import Sheep, Dose, Farm

SAUS = [
    {
        'name': 'britanna',
        'birth_date_utc': datetime.now(),
        'sex': 'f',
    },
    {
        'name': 'lolcakes',
        'birth_date_utc': datetime.now(),
        'sex': 'f',
        'ear_tag': '2608',
        'ear_tag_color': 'r',
        'quality': 'e+',
    },
    {
        'name': 'rambo',
        'birth_date_utc': datetime.now(),
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


def get_all_sheep(request, *, filter_=None):
    if request.user.is_superuser:
        a = Sheep.objects.all()
        if len(a) == 0:
            __init()
            a = Sheep.objects.all()
        all_ = a
    else:
        all_ = Sheep.objects.all().filter(farm__farmers__in=[request.user])
    if filter_ is None:
        return all_
    return all_.filter(**filter_)


@login_required
def index(request):
    prod_sheep = get_all_sheep(request, filter_={'dead__isnull': True,
                                                 'removed__isnull': True})
    dead_sheep = [s for s in get_all_sheep(request) if s not in prod_sheep]
    return TemplateResponse(request, 'index.html', context={'prod_sheep': prod_sheep,
                                                            'dead_sheep': dead_sheep})


@login_required
def sau(request, slug=""):
    if request.user.is_superuser:
        sheep = get_object_or_404(Sheep, slug=slug)
    else:
        sheep = get_object_or_404(Sheep, slug=slug,
                                  farm__farmers__in=[request.user])
    doses = Dose.get(sheep=sheep)
    return TemplateResponse(request, 'sau.html', context={'sheep': sheep,
                                                          'doses': doses})
