from datetime import datetime as dt
from django.contrib.auth.models import User
from django.test import TestCase, Client
from sau.models import Sheep, Farm, Medicine, Dose


def date(y=2010, m=1, d=1, h=6, min_=0, sec=0):
    return dt(y, m, d, h, min_, sec)


SAUS = [
    {
        'name': 'britanna',
        'birth_date_utc': date(),
        'sex': 'f',
    },
    {
        'name': 'lolcakes',
        'birth_date_utc': date(),
        'sex': 'f',
        'ear_tag': '2608',
        'ear_tag_color': 'r',
        'quality': 'e+',
    },
    {
        'name': 'rambo',
        'birth_date_utc': date(),
        'sex': 'm',
        'quality': 'p-',
    },
    {
        'name': 'rb_a',
        'birth_date_utc': date(2012),
        'sex': 'm',
        'quality': 'r',
        'weight': 12.0,
        'fat_percentage': 0.8,
        'dead': date(2014),
    },
    {
        'name': 'rb_b',
        'birth_date_utc': date(2012),
        'sex': 'm',
        'quality': 'u',
        'weight': 10.1,
        'fat_percentage': 0.8,
        'dead': date(2014),
    },
    {
        'name': 'rb_c',
        'birth_date_utc': date(2012),
        'sex': 'f',
        'quality': 'e',
        'weight': 12.0,
        'fat_percentage': 0.8,
    },
    {
        'name': 'rb_c_a',
        'birth_date_utc': date(2013),
        'sex': 'm',
        'quality': 'r',
        'weight': 6.0,
        'fat_percentage': 0.2,
    },
    {
        'name': 'rb_c_b',
        'birth_date_utc': date(2013),
        'sex': 'm',
        'quality': 'u',
        'weight': 7.0,
        'fat_percentage': 0.3,
    },
    {
        'name': 'rb_c_c',
        'birth_date_utc': date(2013),
        'sex': 'm',
        'quality': 'e',
        'weight': 8.0,
        'fat_percentage': 0.4,
    },
]


def get_sheep(names):
    return [Sheep.objects.get(name=n) for n in names]


def generate_test_db():
    for sau in SAUS:
        sau['farm'] = Farm.objects.all()[0]
        s = Sheep.objects.create(**sau)
        s.save()
    r, b = get_sheep(['rambo', 'britanna'])
    rb_a = Sheep.objects.get(name='rb_a')
    rb_b = Sheep.objects.get(name='rb_b')
    rb_c = Sheep.objects.get(name='rb_c')
    for s in (rb_a, rb_b, rb_c):
        s.father = r
        s.mother = b
        s.save()
    rb_c_a = Sheep.objects.get(name='rb_c_a')
    rb_c_b = Sheep.objects.get(name='rb_c_b')
    rb_c_c = Sheep.objects.get(name='rb_c_c')
    for s in (rb_c_a, rb_c_b, rb_c_c):
        s.father = r
        s.mother = rb_c
        s.save()

    username = 'Smeagol'
    password = 'myprecious'
    user = User.objects.create_user(username=username, password=password)
    farm = Farm.objects.all()[0]
    farm.farmers.add(user)
    farm.save()
