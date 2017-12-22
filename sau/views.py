# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime as dt

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404

from sau.models import Sheep, Dose, Farm
from .forms import DoseForm
from .statistics import get_statistics

# SAUS exists solely to populate an empty DB with some stuff.  Will be removed.
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


def _get_sheep_or_404(request, slug):
    if request.user.is_superuser:
        return get_object_or_404(Sheep, slug=slug)

    return get_object_or_404(
        Sheep, slug=slug, farm__farmers__in=[request.user])


@login_required
def sau(request, slug=""):
    sheep = _get_sheep_or_404(request, slug)
    doses = Dose.get(sheep=sheep)
    return TemplateResponse(
        request, 'sau.html', context={
            'sheep': sheep,
            'doses': doses
        })


@login_required
def _save_dose(request, slug):
    form = DoseForm(request.POST)
    if form.is_valid():
        dose = form.save(commit=False)
        dose.sheep = _get_sheep_or_404(request, slug)
        h, m = dt.now().hour, dt.now().minute
        dose.date_utc = dose.date_utc.replace(hour=h, minute=m, second=0)
        dose.save()
    else:
        raise ValueError('Invalid form for dose: %s' % str(request.POST))


@login_required
def dose(request, slug=''):
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
def tree(request, slug=''):  # genealogy
    current_sheep = _get_sheep_or_404(request, slug)
    subtree = current_sheep.children_tree

    # statistics
    dead = [s for s in subtree if s.dead is not None]
    body_count = len(dead)
    qs, ql, ws, wl, ls, ll = get_statistics(dead, subtree)

    prod_children = [s for s in subtree if s.alive]
    dead_children = [s for s in subtree if s not in prod_children]

    return TemplateResponse(
        request, 'genealogy.html', context={
            'sheep': current_sheep,
            'prod_children': prod_children,
            'dead_children': dead_children,
            'number_dead': body_count,
            'qualities': qs,
            'quality_labels': ql,
            'weights': ws,
            'weight_labels': wl,
            'lamb_per_year_lst': ls,
            'lamb_per_year_labels': ll,
        })
