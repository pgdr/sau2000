from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^stats$', views.stats, name='stats'),  # this can later be stats/2016
    url(r'^sau/(?P<slug>[-\w]{1,255})$', views.sau, name='sau'),
    url(r'^sau/(?P<slug>[-\w]{1,255})/dose', views.dose, name='dose'),
    url(r'^sau/(?P<slug>[-\w]{1,255})/tree', views.tree, name='tree'),
]
