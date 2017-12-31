# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime as dt

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from sau.models import Sheep, Dose, Farm

from .statistics import (get_statistics, get_statplots, get_born_per_year,
                         get_weight_per_year)

from .views_util import _get_sheep_or_404
from .views_editors import add_dose, create_or_edit_sheep, add_sheep_batch


def get_all_sheep(request, *, filter_=None):
    if request.user.is_superuser:
        all_ = Sheep.objects.all().order_by('birth_date_utc')
    else:
        all_ = Sheep.objects.all().order_by('birth_date_utc').filter(
            farm__farmers__in=[request.user])
    if filter_ is None:
        return all_
    return all_.filter(**filter_)


@login_required
def index(request):
    prod_sheep = get_all_sheep(
        request, filter_={
            'dead__isnull': True,
            'removed__isnull': True
        })
    dead_sheep = [s for s in get_all_sheep(request) if s not in prod_sheep]
    return TemplateResponse(
        request,
        'index.html',
        context={
            'prod_sheep': prod_sheep,
            'dead_sheep': dead_sheep
        })


@login_required
def sau(request, slug="", sheep_id=None):
    current_sheep = _get_sheep_or_404(request, slug, sheep_id)
    doses = Dose.get(sheep=current_sheep)

    subtree = current_sheep.children_tree

    # statistics
    dead = [s for s in subtree if s.dead is not None]
    svgs = get_statplots(dead, subtree)
    stat = get_statistics(dead, subtree)

    prod_children = [s for s in subtree if s.alive]
    dead_children = [s for s in subtree if s not in prod_children]

    return TemplateResponse(
        request,
        'sau.html',
        context={
            'sheep': current_sheep,
            'prod_children': prod_children,
            'dead_children': dead_children,
            'stats': stat,
            'svgs': svgs,
            'doses': doses,
        })



@login_required
def stats(request):
    all_sheep = Sheep.objects.all()
    if not request.user.is_superuser:
        all_sheep = all_sheep.filter(farm__farmers__in=[request.user])

    born_stat = get_born_per_year(all_sheep)
    weight_stat = get_weight_per_year(all_sheep)

    prod = [s for s in all_sheep if s.alive]
    dead = [s for s in all_sheep if s not in prod]

    return TemplateResponse(
        request,
        'stats.html',
        context={
            'prod': prod,
            'dead': dead,
            'born': born_stat,
            'weight': weight_stat,
        })


@login_required
def search(request):
    q = request.GET.get('q', '')  # the query
    s = request.GET.get('s', 'all')  # the status in (all, prod, noprod)
    if s not in ('all', 'prod', 'noprod'):
        s = 'all'

    all_sheep = get_all_sheep(request)
    all_sheep = all_sheep.filter(name__icontains=q) | all_sheep.filter(
        ear_tag__icontains=q)

    prod_sheep = all_sheep.filter(**{
        'dead__isnull': True,
        'removed__isnull': True
    })
    dead_sheep = all_sheep.filter(dead__isnull=False) | all_sheep.filter(
        removed__isnull=False)

    if s == 'prod':
        dead_sheep = []
    elif s == 'noprod':
        prod_sheep = []


    return TemplateResponse(
        request,
        'index.html',
        context={
            'prod_sheep': prod_sheep,
            'dead_sheep': dead_sheep,
            'is_search': True,
            'search_results': len(prod_sheep) + len(dead_sheep),
        })
