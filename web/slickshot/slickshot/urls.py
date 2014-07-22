from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.index),

    url(r'^shoot$', views.shoot),
    url(r'^status$', views.status),
    url(r'^share$', views.share),

    url(r'^uuid$', views.generate_uuid),
)
