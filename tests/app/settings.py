"""
Django settings for app project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import os

import django


# placeholder for gettext
def _(s): return s

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j#zwt2c!*(7(jz!m(tr$+jq^1d(+)e(^059f^nd_(*zj!gv0x)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'modeltranslation',
    # 'grappelli',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',

    'app'
)

if django.get_version() >= '1.7':
    INSTALLED_APPS += (
        'mtr.sync',
    )
else:
    INSTALLED_APPS += (
        'mtr_sync',
    )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

if django.get_version() >= '1.7':
    MIDDLEWARE_CLASSES += (
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    )
else:
    INSTALLED_APPS += (
        'south',
    )
    SOUTH_MIGRATION_MODULES = {
        'app': 'app.south_migrations',
        'mtr.sync': 'sync.south_migrations'
    }

MIDDLEWARE_CLASSES += (
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

if django.get_version() >= '1.8':
    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.template.context_processors.debug",
        "django.template.context_processors.i18n",
        "django.template.context_processors.media",
        "django.template.context_processors.static",
        "django.template.context_processors.tz",
        'django.template.context_processors.request',
        "django.contrib.messages.context_processors.messages"
    )
else:
    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.tz",
        'django.core.context_processors.request',
        "django.contrib.messages.context_processors.messages"
    )

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'olddb.sqlite3'),
    }
}

if django.get_version() >= '1.7':
    DATABASES['default']['NAME'] = os.path.join(BASE_DIR, 'db.sqlite3')

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('de', _('German')),
    ('en', _('English')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Celery settings
BROKER_BACKEND = 'memory'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True


SYNC_SETTINGS = {
    'ACTIONS': ['mtr.sync.lib.actions', 'app.sync']
}
