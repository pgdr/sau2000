# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404

from sau.models import Sheep, Dose

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
    for sau in SAUS:
        s = Sheep.objects.create(**sau)
        s.save()


def get_all_sheep():
    a = Sheep.objects.all()
    if len(a) == 0:
        __init()
        a = Sheep.objects.all()
    return a


@login_required
def index(request):
    sheep = get_all_sheep()
    return TemplateResponse(request, 'index.html', context={'sheep': sheep})


@login_required
def sau(request, slug=""):
    sheep = get_object_or_404(Sheep, slug=slug)
    doses = Dose.get(sheep=sheep)
    return TemplateResponse(request, 'sau.html', context={'sheep': sheep,
                                                          'doses': doses})
