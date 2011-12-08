from os.path import dirname, abspath, join
from django.conf.urls.defaults import *
from django.conf import settings

if settings.DEBUG:
    urlpatterns = patterns('',
        #static content
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':join(dirname(abspath(__file__)), 'media')}, name='media'),
)