# -*- coding: utf-8 -*-

from sau.models import Farm

def add_farm(request):
    u = request.user
    farms = Farm.objects.all().filter(farmers__in=[u])
    if len(farms) == 0:
        raise LookupError("%s did not belong to any farm." % u.username)
    return {
        'farm': farms[0]
    }