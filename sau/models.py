# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


QUALITIES = (
    ('e', 'E'), ('e-', 'E-'), ('e+', 'E+'),
    ('u', 'U'), ('u-', 'U-'), ('u+', 'U+'),
    ('r', 'R'), ('r-', 'R-'), ('r+', 'R+'),
    ('o', 'O'), ('o-', 'O-'), ('o+', 'O+'),
    ('p', 'P'), ('p-', 'P-'), ('p+', 'P+'),
)

SEXES = (
    ('m', 'Ram'),
    ('f', 'Ewe'),
)

class Sheep(models.Model):
    ear_tag = models.CharField(max_length=100)
    birth_date_utc = models.DateTimeField('born', auto_now_add=False)
    name = models.CharField(max_length=100)
    main_picture = models.ImageField()
    quality = models.CharField(max_length=2, choices=QUALITIES, blank=True)
    fat_percentage = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    sex = models.CharField(max_length=1, choices=SEXES)
    mother = models.ManyToManyField('self')
    father = models.ManyToManyField('self')
