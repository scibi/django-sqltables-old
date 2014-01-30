from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import sqltables
sqltables.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'demo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tables/', include(sqltables.manager.urls)),
)
