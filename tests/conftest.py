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
        IP_RESTRICTOR_SKIP_CHECK_SENDER_ID='sender-debug',
        IP_RESTRICTOR_SKIP_CHECK_SECRET='secret-debug',
        RESTRICTED_APP_NAMES=['admin'],
        ALLOWED_ADMIN_IPS=[],
        DIRECTORY_CONSTANTS_URL_EXPORT_READINESS='https://exred.com',
        DIRECTORY_CONSTANTS_URL_EXPORT_OPPORTUNITIES='https://exopps.com',
        DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS='https://soo.com',
        DIRECTORY_CONSTANTS_URL_EVENTS='https://events.com',
        DIRECTORY_CONSTANTS_URL_INVEST='https://invest.com',
        DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER='https://fas.com',
        DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON='https://sso.com',
        DIRECTORY_CONSTANTS_URL_FIND_A_BUYER='https://fab.com',
    )


@pytest.fixture(autouse=True)
def reset_urlsconf():
    set_urlconf('tests.urls')
