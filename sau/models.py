# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model


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


def _children(parent):
    for sheep in Sheep.objects.all():
        if parent in (sheep.mother, sheep.father):
            yield sheep


class Farm(models.Model):
    name = models.CharField(max_length=256)
    farmers = models.ManyToManyField(get_user_model())

    def __repr__(self):
        return 'Farm(name=%s)' % self.name

    def __str__(self):
        return str(self.name)


class Sheep(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=40, blank=True, editable=False)
    ear_tag = models.CharField(max_length=30, blank=True)
    ear_tag_color = models.CharField(max_length=1, choices=COLOR, default='w')
    birth_date_utc = models.DateTimeField(
        'born', null=True, blank=True, auto_now_add=False)
    main_picture = models.ImageField(blank=True)
    quality = models.CharField(max_length=2, choices=QUALITIES, blank=True)
    fat_percentage = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEXES)
    mother = models.ForeignKey(
        'Sheep',
        related_name='a_mother',
        null=True,
        blank=True,
        on_delete=models.PROTECT)
    father = models.ForeignKey(
        'Sheep',
        related_name='a_father',
        null=True,
        blank=True,
        on_delete=models.PROTECT)
    dead = models.DateTimeField(
        'death', null=True, blank=True, auto_now_add=False)
    removed = models.DateTimeField(
        'removed', null=True, blank=True, auto_now_add=False)
    origin = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    farm = models.ForeignKey('Farm', on_delete=models.PROTECT,
                             default=None)

    @property
    def alive(self):
        return not self.dead and not self.removed

    @property
    def colored_tag(self):
        return self.ear_tag_color, self.ear_tag

    @property
    def children(self):
        return list(_children(self))

    @property
    def children_tree(self):
        seen = set()
        queue = [self]
        res = set()
        while queue:
            n = queue.pop()
            cn = _children(n)
            for s in cn:
                res.add(s)
                if s not in seen:
                    seen.add(s)
                    queue.append(s)
        return res

    def __repr__(self):
        return 'Sheep(name=%s)' % self.name

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Sheep, self).save(*args, **kwargs)


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        if not self.description:
            return str(self.name)
        return '%s (%s)' % (self.name, self.description)

    def __repr__(self):
        return 'Medicine(%s)' % str(self)


class Dose(models.Model):
    """One Dose is some amount (millilitres) of Medicine given to a Sheep."""
    medicine = models.ForeignKey('Medicine', on_delete=models.PROTECT)
    sheep = models.ForeignKey('Sheep', on_delete=models.PROTECT)
    amount = models.FloatField(default=25)
    date_utc = models.DateTimeField(
        'given', null=True, blank=True, auto_now_add=False)

    def __str__(self):
        return 'Dose(%s -> %s [%.2f])' % (repr(self.medicine),
                                          repr(self.sheep), self.amount)

    @classmethod
    def get(cls, **kwargs):
        return Dose.objects.all().filter(**kwargs).order_by('-date_utc')
