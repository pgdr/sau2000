# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

#from sau.models import Sheep

def index(request):
    return HttpResponse("Hello, world.")
