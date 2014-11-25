# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*e_x1qszxuff4oq)7aq*&-*iop=i)3p0w(vpwm*3v_klm#@!q$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

CRISPY_TEMPLATE_PACK = 'bootstrap3'
GRAPPELLI_ADMIN_TITLE = 'RDS'

FILE_UPLOAD_PERMISSIONS = 0755

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli',
    'django.contrib.admin',
    'gunicorn',
    'crispy_forms',
    'django_password_strength',
    'rds',
    'async_messages',
    'djangobower',
    'caboskin'
)

BOWER_INSTALLED_APPS = (
    'jquery#1.9',
    'jquery-ui#1.10',
    'bootstrap#3.1.0',
    'flat-ui',
    'html5shiv',
    'respond',
    'zxcvbn',
    'spin.js'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'djangobower.finders.BowerFinder',
    )

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components')

ROOT_URLCONF = 'rds.urls'

WSGI_APPLICATION = 'rds.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = '/srv/samba'

PACKAGE_DIR = MEDIA_ROOT
TEST_PACKAGE_DIR = BASE_DIR + '/software_test'

SAMBA_SHARE = r'\\ubuntu\share'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = BASE_DIR + '/static'

STATIC_URL = '/static/'
MEDIA_URL = '/uploads/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
            },
        'file': {
            'level':'DEBUG',
            'class':'logging.FileHandler',
            # 'filename': '/var/log/gunicorn/django.log',
            'filename': 'django.log',
            'formatter':'verbose'
            }
    },
    'loggers': {
        '':{
            'handlers': ['console', 'file'],
            'level': 'INFO'
        },
        'django': {
            'handlers': ['console', 'file'],
            'propagate': False,
            'level': 'INFO',
        },
        'rds': {
            'handlers': ['console', 'file'],
            'propagate': False,
            'level': 'DEBUG'
        }
    }
}

from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'rds.context_processors.servers',
    'async_messages.context_processors.unread'
)

if DEBUG:
    # DEBUG_TOOLBAR_PATCH_SETTINGS = False
    # DBar is skipped if INTERNAL_IP doesn't match the requests
    # bypass that
    def always_true(request):
        return True

    INSTALLED_APPS += (
        'debug_toolbar',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': "%s.always_true" % __name__,
    }
