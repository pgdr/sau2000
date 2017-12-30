from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^stats$', views.stats, name='stats'),  # this can later be stats/2016
    url(r'^new/', views.create_or_edit_sheep, name='new_sheep'),
    url(r'^sau/(?P<slug>[-\w]{1,255})/(?P<sheep_id>\d+)$', views.sau, name='sau'),
    url(r'^sau/(?P<slug>[-\w]{1,255})/(?P<sheep_id>\d+)/dose', views.add_dose, name='dose'),
    url(r'^sau/(?P<slug>[-\w]{1,255})/(?P<sheep_id>\d+)/edit', views.create_or_edit_sheep, name='edit_sheep'),
    url(r'^search$', views.search, name='search'),
]
