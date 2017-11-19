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

COLOR = (
    ('r', 'Red'),
    ('w', 'White'),
    ('y', 'Yellow'),
    ('g', 'Green'),
    ('b', 'Blue'),
    ('a', 'Gray'),
    ('c', 'Cyan'),
    ('k', 'Black'),
)

class Sheep(models.Model):
    ear_tag = models.CharField(max_length=100)
    ear_tag_color = models.CharField(max_length=1, choices=COLOR, default='w')
    birth_date_utc = models.DateTimeField('born', auto_now_add=False)
    name = models.CharField(max_length=100)
    main_picture = models.ImageField()
    quality = models.CharField(max_length=2, choices=QUALITIES, blank=True)
    fat_percentage = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    sex = models.CharField(max_length=1, choices=SEXES)
    mother = models.ForeignKey('Sheep',
                               related_name='a_mother',
                               null=True,
                               on_delete=models.PROTECT)
    father = models.ForeignKey('Sheep',
                               related_name='a_father',
                               null=True,
                               on_delete=models.PROTECT)

    @property
    def alive(self):
        return not self.quality

    @property
    def colored_tag(self):
        return self.ear_tag_color, self.ear_tag

    def __repr__(self):
        return 'Sheep(name=%s)' % self.name
