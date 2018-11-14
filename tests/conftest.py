import pytest

from django.urls import set_urlconf


def pytest_configure():
    from django.conf import settings
    settings.configure(
        ALLOWED_HOSTS=['*'],
        ROOT_URLCONF='tests.urls',
        SSO_PROXY_LOGIN_URL='http://login.com',
        SSO_PROXY_SIGNUP_URL='http://signup.com',
        SSO_PROXY_LOGOUT_URL='http://logout.com',
        SSO_PROFILE_URL='http://profile.com',
        FEATURE_FLAGS={
            'SEARCH_ENGINE_INDEXING_OFF': True,
            'MAINTENANCE_MODE_ON': False,
        },
        INSTALLED_APPS=[
            'django.contrib.staticfiles',
            'directory_components',
        ],
        STATIC_URL='/static/',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'OPTIONS': {
                    'loaders': [
                        'django.template.loaders.app_directories.Loader',
                    ],
                },
            },
        ],
        FEATURE_URL_PREFIX_ENABLED=True,
        URL_PREFIX_DOMAIN='',
    )


@pytest.fixture(autouse=True)
def reset_urlsconf():
    set_urlconf('tests.urls')
