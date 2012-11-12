from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('crime.views',
    url(r'^$', 'index'),
    #url(r'^crime/reboot/$', 'reboot'),
    #url(r'^crime/reboot/handler/$', 'rebootHandler'),
    url(r'^crime/type/(\d+)/$', 'getCrimeType'),
    url(r'^crime/type/(\d+).json$', 'getCrimeDataJSON'),
    url(r'^crime/all.json$', 'getCrimeTypesJSON'),
)

urlpatterns += patterns('polls.views',
    url(r'^polls/$', 'index'),
    url(r'^polls/(?P<poll_id>\d+)/$', 'detail'),
    url(r'^polls/(?P<poll_id>\d+)/results/$', 'results'),
    url(r'^polls/(?P<poll_id>\d+)/vote/$', 'vote'),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

"""
urlpatterns = patterns('',

    url(r'^polls/$', 'polls.views.index'),
    url(r'^polls/(?P<poll_id>\d+)/$', 'polls.views.detail'),
    url(r'^polls/(?P<poll_id>\d+)/results/$', 'polls.views.results'),
    url(r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
    #url(r'^polls/latest\.php$', 'polls.views.index')

    # Examples:
    # url(r'^$', 'opendata.views.home', name='home'),
    # url(r'^opendata/', include('opendata.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
"""