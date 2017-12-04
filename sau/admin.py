# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django import forms

# Register your models here.
from .models import Sheep, Medicine, Dose


# To get gender-aware dropdown list for parent of a sheep
class SheepParentForm(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "father":
            kwargs["queryset"] = Sheep.objects.filter(sex='m')  # male
        elif db_field.name == "mother":
            kwargs["queryset"] = Sheep.objects.filter(sex='f')  # female
        return super(SheepParentForm, self).formfield_for_foreignkey(db_field,
                                                                     request,
                                                                     **kwargs)


admin.site.register(Sheep, SheepParentForm)
admin.site.register(Medicine)
admin.site.register(Dose)
