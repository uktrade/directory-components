# -*- coding: utf-8 -*-

"""
Django settings for ui project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import environ


env = environ.Env()
for env_file in env.list('ENV_FILES', default=[]):
    env.read_env(f'demo/conf/env/{env_file}')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

# As the app is running behind a host-based router supplied by PaaS, we can open ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']

# https://docs.djangoproject.com/en/dev/ref/settings/#append-slash
APPEND_SLASH = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'demo',
    'directory_components',
    'directory_components.janitor',
]

MIDDLEWARE = [
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'directory_components.middleware.LocaleQuerystringMiddleware',
    'directory_components.middleware.PersistLocaleMiddleware',
    'directory_components.middleware.ForceDefaultLocale',
    'directory_components.middleware.CountryMiddleware',
]

ROOT_URLCONF = 'demo.conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'directory_components.context_processors.header_footer_processor',
                'directory_components.context_processors.urls_processor',
                'directory_components.context_processors.sso_processor',
                'directory_components.context_processors.cookie_notice',
                'directory_components.context_processors.feature_flags',
            ],
        },
    },
]

# Static files served with Whitenoise and AWS Cloudfront
# http://whitenoise.evans.io/en/stable/django.html#instructions-for-amazon-cloudfront
# http://whitenoise.evans.io/en/stable/django.html#restricting-cloudfront-to-static-files
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_HOST = env.str('STATIC_HOST', '')
STATIC_URL = STATIC_HOST + '/static/'
STATICFILES_STORAGE = env.str(
    'STATICFILES_STORAGE',
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_L10N = True
USE_TZ = True

# https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-LANGUAGE_COOKIE_NAME
LANGUAGE_COOKIE_DEPRECATED_NAME = 'django-language'
# Django's default value for LANGUAGE_COOKIE_DOMAIN is None
LANGUAGE_COOKIE_DOMAIN = env.str('LANGUAGE_COOKIE_DOMAIN', None)

LANGUAGE_COOKIE_SECURE = env.bool('LANGUAGE_COOKIE_SECURE', True)
COUNTRY_COOKIE_SECURE = env.bool('COUNTRY_COOKIE_SECURE', True)

# https://github.com/django/django/blob/master/django/conf/locale/__init__.py
LANGUAGES = [
    ('en-gb', 'English'),    # English
    ('de', 'Deutsch'),       # German
    ('ja', '日本語'),         # Japanese
    ('zh-hans', '简体中文'),  # Simplified Chinese
    ('fr', 'Français'),      # French
    ('es', 'español'),       # Spanish
    ('pt', 'Português'),     # Portuguese
    ('ar', 'العربيّة'),          # Arabic
]

LOCALE_PATHS = (
    os.path.abspath(os.path.join(BASE_DIR, '../directory_components/locale')),
)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# Logging for development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'mohawk': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'requests': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

# security
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC = env.str(
    'DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC', ''
)
DIRECTORY_CONSTANTS_URL_INTERNATIONAL = env.str(
    'DIRECTORY_CONSTANTS_URL_INTERNATIONAL', ''
)
DIRECTORY_CONSTANTS_URL_INVEST = env.str(
    'DIRECTORY_CONSTANTS_URL_INVEST', ''
)
DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS = env.str(
    'DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS', ''
)
DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER = env.str(
    'DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER', ''
)
PRIVACY_COOKIE_DOMAIN = env.str('PRIVACY_COOKIE_DOMAIN', '')

# feature flags
FEATURE_FLAGS = {
    'COUNTRY_SELECTOR_ON': env.bool('FEATURE_COUNTRY_SELECTOR_ENABLED', False)
}

SSO_PROXY_SIGNUP_URL = 'https://signup.com'
SSO_PROXY_LOGIN_URL = 'https://login.com'
SSO_PROXY_LOGOUT_URL = 'https://logout.com'
SSO_PROFILE_URL = 'https://profile.com'