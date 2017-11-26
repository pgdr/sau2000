# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Sheep, Medicine, Dose
admin.site.register(Sheep)
admin.site.register(Medicine)
admin.site.register(Dose)
