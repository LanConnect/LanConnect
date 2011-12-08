from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^LanConnect/', include('LanConnect.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
    (r'^$', lambda r: direct_to_template(request, "home.html")),
    
    (r'^admin/', include(admin.site.urls)),
                        
    (r'^board/', include('sphene.sphboard.urls')),
                       
    (r'^(?P<urlPrefix>test/(?P<groupName>\w+))/board/', include('sphene.sphboard.urls')),
    (r'^(?P<urlPrefix>test/(?P<groupName>\w+))/wiki/',  include('sphene.sphwiki.urls')),

    #(r'^wiki/',  include('sphene.sphwiki.urls'), { 'urlPrefix': 'wiki', 'groupName': 'Sphene' }),

    (r'^static/sphene/(.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/../../communitytools/static/sphene' }),
    #(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/../static' }),

    #(r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': '/home/kahless/dev/python/diamanda/media'}), # change it or remove if not on dev server

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$','django.contrib.auth.views.logout'),
    (r'^accounts/register/(?P<emailHash>[a-zA-Z/\+0-9=]+)/$', 'sphene.community.views.register_hash'),
                       
#    (r'^forum/', include('myghtyboard.URLconf')), # forum
#    (r'^muh/', 'wiki.views.show_page'), # wiki main page under /
#    (r'^wiki/', include('wiki.URLconf')), # wiki
#    (r'^wiki/feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}), # wiki feeds
#    (r'^wiki/sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}), # wikiPages sitemap

)
