from django.shortcuts import get_object_or_404
from sau.models import Sheep


def _get_sheep_or_404(request, slug):
    if request.user.is_superuser:
        return get_object_or_404(Sheep, slug=slug)

    return get_object_or_404(
        Sheep, slug=slug, farm__farmers__in=[request.user])
