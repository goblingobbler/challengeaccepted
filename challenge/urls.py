from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'home.views.index', name='index'),
    url(r'^likes/', include('likes.urls')),

    url(r'^challenges/', 'home.views.challenges', name='challenges'),
	url(r'^filter/', 'home.views.filter', name='filter'),

	url(r'^edit/', 'home.views.edit', name='edit'),
	url(r'^comment/([0-9]+)/', 'home.views.comment', name='comment'),
	url(r'^challenge/([0-9]+)/', 'home.views.viewchallenge', name='challenge'),
	

    url(r'^admin/', include(admin.site.urls)),
)
