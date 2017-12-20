# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Sheep, Medicine, Dose, Farm


class FarmAwareModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(farm__farmers__in=[request.user])


class SheepForm(FarmAwareModelAdmin):
    """Sheep form, for overriding various fields in admin panel.

    Today we override:
       * father and mother --- make them gender aware
       * farm --- make field (super)user aware
    """

    # To get gender-aware dropdown list for parent of a sheep
    def sheep_parent_filter(self, db_field, request, **kwargs):
        filters = {}
        if db_field.name == 'father':
            filters['sex'] = 'm'  # male
        elif db_field.name == 'mother':
            filters['sex'] = 'f'  # female
        else:
            raise RuntimeError(
                'Filter called on wrong field: %s' % str(db_field.name))
        kwargs['queryset'] = Sheep.objects.filter(**filters)
        return super(SheepForm, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    # To get user-aware dropdown list for farm of a sheep
    def farm_filter(self, db_field, request, **kwargs):
        filters = {}
        if not request.user.is_superuser:
            filters['farm__farmers__in'] = [request.user]
        kwargs['queryset'] = Farm.objects.filter(**filters)
        return super(SheepForm, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    # this is the method we're overriding, but only on fields
    # * mother/father
    # * farm
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ('father', 'mother'):
            return self.sheep_parent_filter(db_field, request, **kwargs)

        if db_field.name == 'farm':
            return self.farm_filter(db_field, request, **kwargs)
        return super(SheepForm, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


admin.site.register(Sheep, SheepForm)
admin.site.register(Medicine)
admin.site.register(Dose)
admin.site.register(Farm, FarmAwareModelAdmin)
