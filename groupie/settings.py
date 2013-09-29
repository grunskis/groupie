# -*- coding: utf-8 -*-
import os

import dj_database_url


DEBUG = os.environ.get('DEBUG', False)
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Martins Grunskis', 'martins@grunskis.com'),
    ('Mateusz Jankowski', 'mat.jankowski@gmail.com')
)

MANAGERS = ADMINS

DATABASES = {'default': dj_database_url.config()}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
)

TIME_ZONE = 'Europe/Berlin'

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

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['SECRET_KEY']

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
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'groupie.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'groupie.wsgi.application'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'pipeline',
    'twitter_bootstrap',
    'bootstrapform',
    'raven.contrib.django.raven_compat',
    'jstemplate',

    'groupie.app'
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

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
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'

MAILGUN_SERVER_NAME = 'groupie.mailgun.org'
MAILGUN_ACCESS_KEY = os.environ['MAILGUN_API_KEY']

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.jsmin.JSMinCompressor'
PIPELINE_CSS_COMPRESSOR = None

#PIPELINE_ENABLED = True

PIPELINE_CSS = {
    'bootstrap': {
        'source_filenames': (
            'lib/bootstrap/css/bootstrap.min.css',
            'lib/bootstrap/css/datetimepicker.css',
            'lib/bootstrap/css/Sprites.min.css',
            'lib/bootstrap/css/bootstrap-tagsinput.css'
        ),
        'output_filename': 'css/bootstrap.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'groupie': {
        'source_filenames': (
            'css/style.css',
        ),
        'output_filename': 'css/groupie.css',
        'extra_context': {
            'media': 'screen,projection',
        }
    }
}

PIPELINE_JS = {
    'bootstrap': {
        'source_filenames': (
          'js/transition.js',
          'js/modal.js',
          'js/dropdown.js',
          'js/scrollspy.js',
          'js/tab.js',
          'js/tooltip.js',
          'js/popover.js',
          'js/alert.js',
          'js/button.js',
          'js/collapse.js',
          'js/carousel.js',
          'js/affix.js',
        ),
        'output_filename': 'js/bootstrap.js',
    },
    'libs': {
        'source_filenames': (
            'lib/mustache.js',
            'libs/django.mustache.js',
            'js/bootstrap-datetimepicker.js',
            'js/bootstrap-tagsinput.js',
            'js/pluralize.js'
        ),
        'output_filename': 'js/libs.js'
    },
    'groupie': {
        'source_filenames': (
            'js/app.js',
            'js/voting.js',
        ),
        'output_filename': 'js/groupie.js'
    }
}

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
}
