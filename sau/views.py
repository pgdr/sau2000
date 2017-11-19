# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from sau.models import Sheep

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


def html(tag, content):
    return '<{tag}>\n\t{content}\n</{tag}>'.format(tag=tag, content=content)


def ul(lst, ordering='ul'):
    li = lambda x: html('li', x)
    return html(ordering, ''.join(map(li, lst)))


def index(request):
    sheep = get_all_sheep()
    names = [s.name for s in sheep]

    content = html('h1', 'Sau2000')
    content += ul(names)
    content += html('p', 'the end.')

    return HttpResponse(content)
