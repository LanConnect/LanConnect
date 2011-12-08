import os, sys
ROOT_PATH = os.path.dirname(os.path.abspath('settings.py'))
sys.path.append(ROOT_PATH)
sys.path.append(os.path.join(ROOT_PATH, '..','..', 'CommunityTools', 'sphenecoll'))

DEBUG=True

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

ADMINS = (
          ('Firstyear', 'firstyear@internode.on.net'),
          ('Micolous', 'micolous@gmail.com'),
          ('tWoolie', 'woolford.thomas@gmail.com'),
          )

DATABASES = {'default':
             {
              'ENGINE':'django.db.backends.sqlite3',
              'NAME': 'test.db', 
              }
             }

LDAP_AUTH_SETTINGS = (
                      {'url': 'ldap://ldap.example.com',
                       'bindname' : 'someuser',
                       'realm': 'EXAMPLE.COM',
                      },
                     )
