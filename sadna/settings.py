# Django settings for sadna project.
import os

DEBUG = True
DB_DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

if DB_DEBUG == False :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'giladprojsadna',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'sadnaproj',
            'PASSWORD': 'xsbv',
            'HOST': '162.13.104.169',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '3306',                      # Set to empty string for default.
        }
    }
else :
    DATABASES = { 
        'default': {        
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'projectsadna',  # Or path to database file if using sqlite3.
            'USER': 'root',  # Not used with sqlite3.
            'PASSWORD': '',  # Not used with sqlite3.
            'HOST': '127.0.0.1',  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
        }
    }
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

SETTINGS_ROOT = os.path.dirname(__file__)
LOGFILE_ROOT = SETTINGS_ROOT

#MEDIA_ROOT = os.path.join(SETTINGS_ROOT, "media")
MEDIA_ROOT = "d:\sadna"
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(SETTINGS_ROOT, "static/")

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0av)k5p137r*v1bpv^!4$rr3yygk)54mq9^alw(xud!f-n%vje'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sadna.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'sadna.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'files',
    'general',
    'words',
    'django_extensions',
    'debug_toolbar',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(filename)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },           
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'production_file':{
            'level' : 'INFO',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'when':'midnight',
            'interval':1,
            'filename': LOGFILE_ROOT + 'feedsme_prod.log',
            #'maxBytes': 1024*1024*5, # 5 MB
            'backupCount' : 7,
            'formatter': 'standard',
            'filters': ['require_debug_false'],
        },                          
        'debug_file':{
            'level' : 'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'when':'midnight',
            'interval':1,
            'filename': LOGFILE_ROOT + 'feedsme_debug.log',
            #'maxBytes': 1024*1024*5, # 5 MB
            'backupCount' : 7,
            'formatter': 'standard',
            #'filters': ['require_debug_true'],
        },
        'sql_log': {
            'level':'DEBUG',
            'filters': ['require_debug_true'],
            'class':'logging.handlers.TimedRotatingFileHandler',
            'when':'midnight',
            'interval':1,
            'filename': LOGFILE_ROOT + 'sql_queries.log',
            #'encoding':'bz2',
            #'maxBytes': 1024*1024*10,
            'backupCount': 7,
            'formatter': 'standard',
        }                           
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'handlers': ['production_file', 'debug_file'],
            #'level': 'DEBUG',
        },                
    }
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK':lambda r: not r.META['HTTP_USER_AGENT'].startswith('curl'),
    'INTERCEPT_REDIRECTS':False
}
