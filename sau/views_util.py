from django.http import Http404
from django.shortcuts import get_object_or_404
from sau.models import Sheep

def _get_sheep_or_404(request, slug):
    sheep = _get_sheep(request, slug)
    if sheep is None:
        raise Http404
    return sheep

def _get_sheep(request, slug):
    sheep = None

    kw = {'slug': slug}
    if request.user.is_superuser:
        kw['farm__farmers__in'] = [request.user]

    try:
        sheep = Sheep.objects.get(**kw)
    except Sheep.DoesNotExist:
        pass
    return sheep
