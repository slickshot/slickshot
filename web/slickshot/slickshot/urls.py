from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'slickshot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index)
)
