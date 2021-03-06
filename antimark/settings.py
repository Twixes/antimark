"""Django settings for antimark project."""

import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.getenv('ENV', '').lower().startswith('dev')
INTERNAL_IPS = [
    '127.0.0.1'
]

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

INSTALLED_APPS = [
    'poll.apps.PollConfig',
    'sass_processor',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'antimark.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'antimark.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=not DEBUG) if os.getenv('DATABASE_URL') else {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

AUTH_USER_MODEL = 'poll.School'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SECURE_HSTS_PRELOAD = not DEBUG
SECURE_HSTS_SECONDS = 365 * 24 * 60 * 60 if not DEBUG else 0

LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en-us', 'English'),
    ('pl', 'polski')
]
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_THOUSAND_SEPARATOR = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder'
]

SASS_PRECISION = 8

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['poll.permissions.IsAuthenticatedAndOwnerOrIsStaffOrReadOnly'],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}
