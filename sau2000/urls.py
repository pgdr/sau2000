from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()


# Examples:
# url(r'^$', 'sau2000.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]
