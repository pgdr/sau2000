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


# To get gender-aware dropdown list for parent of a sheep
class SheepParentForm(FarmAwareModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        filters = {}
        if not request.user.is_superuser:
            filters['farm__farmers__in'] = [request.user]
        if db_field.name == 'father':
            filters['sex'] = 'm'  # male
        elif db_field.name == 'mother':
            filters['sex'] = 'f'  # female
        kwargs['queryset'] = Sheep.objects.filter(**filters)
        return super(SheepParentForm, self).formfield_for_foreignkey(db_field,
                                                                     request,
                                                                     **kwargs)


admin.site.register(Sheep, SheepParentForm)
admin.site.register(Medicine)
admin.site.register(Dose)
admin.site.register(Farm, FarmAwareModelAdmin)
