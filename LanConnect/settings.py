# Django settings for LanConnect project.
import os, sys
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_PATH)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

#email Settings
EMAIL_HOST = ( 'mail.internode.on.net' )
DEFAULT_FROM_EMAIL = ( 'development@firstyear.id.au' )

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Australia/Adelaide'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-au'
LANGUAGES = (
#    ('de', 'German'),
    ('en', 'English'),
#    ('fr', 'French'),
#    ('pl', 'Polish'),
#    ('ko', 'Korean'),
#    ('ru', 'Russian'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(ROOT_PATH,'..','static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'y6bz5dlng7(5tvw+tzrqi!cx^wn7k*nx0e%4%y#z-!4xo1q7f4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
##    'sphene.community.groupaware_templateloader.load_template_source',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
##    'sphene.community.context_processors.navigation',
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
#    'sphene.sphboard.middleware.PerformanceMiddleware',
#    'sphene.community.middleware.PsycoMiddleware',
    'sphene.community.middleware.ThreadLocals',
    'sphene.community.middleware.GroupMiddleware',
    'sphene.community.middleware.MultiHostMiddleware',
#    'sphene.community.middleware.StatsMiddleware',
    'sphene.community.middleware.LastModified',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'sphene.community.middleware.PermissionDeniedMiddleware',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH, 'sitetemplates'),
)

INSTALLED_APPS = (
    #must be at the top for maximum awesome (also to intercept admin templates)
    #'fumi',
    
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    
    #'rosetta',
    'debug_toolbar',
    'south',
    'sorl.thumbnail',
    
    #'sphene.community',
    #'sphene.sphboard',
    #'sphene.sphwiki',
    #'sphene.sphblog',
    
    #'joust',
    #'achievements',
    #'events',
)

INTERNAL_IPS = ("127.0.0.1",) #for ddt and sorl

CACHE_BACKEND = 'dummy://'

LOGIN_REDIRECT_URL = '/'

ROOT_URLCONF = 'LanConnect.urls'

SPH_SETTINGS =  {'wiki_rss_url' : '/feeds/wiki/',}
SPH_SETTINGS['community_show_languageswitcher'] = False
# Customize wikilink regex - by default CamelCase would be replaced..
# with this regex only words within [brackets] are replaced.
SPH_SETTINGS['wikilink_regexp'] = r'''((?P<urls><a .*?>.*?</a)|(?P<escape>\\|\b)?(?P<wholeexpression>(\[(?P<snipname>[A-Za-z\-_/0-9]+)(\|(?P<sniplabel>.+?))?\])))'''

DJAPIAN_DATABASE_PATH = os.path.join(ROOT_PATH,'..','cache')

# You can configure this to make every subdomain refer to it's own community 'Group'
SPH_HOST_MIDDLEWARE_URLCONF_MAP = {
    r'^(?P<groupName>\w+).localhost.*$': { 'urlconf': 'urlconfs.community_urls', },
    '.*': { 'urlconf': 'urlconfs.community_urls',
            'params': { 'groupName': 'example' } },
}

#Since LDAP code uses group,dn, to enable our groups to work across many DNs we need to "modify" our code. All groups are prependded by cn=, so we can forget that
AUTHENTICATION_BACKENDS = ('fumi.auth.LDAPBackend',)
AUTH_PROFILE_MODULE = 'community.CommunityUserProfile'

LDAP_AUTH_SETTINGS = ({
    'url' : None,
    'bindname': None,
    'bindpw': None,
    'app_name' : None,
    'realm' : None,
    'memberOf_overlay' : False,
        },)
ACHIEVEMENT_IMAGES_DIRECTORY = 'achievement-images/'

#try:
# settings_local overwrites a few settings from here, and has to define SECRET_KEY
from settings_local import *
#except Exception as e:
#    print "Warning - Error importing settings_local:", e
