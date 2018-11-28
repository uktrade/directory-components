from unittest.mock import Mock

import pytest

from directory_constants.constants import urls
from directory_components import context_processors


def test_analytics(settings):
    settings.GOOGLE_TAG_MANAGER_ID = '123'
    settings.GOOGLE_TAG_MANAGER_ENV = '?thing=1'
    settings.UTM_COOKIE_DOMAIN = '.thing.com'

    actual = context_processors.analytics(None)

    assert actual == {
        'directory_components_analytics': {
            'GOOGLE_TAG_MANAGER_ID': '123',
            'GOOGLE_TAG_MANAGER_ENV': '?thing=1',
            'UTM_COOKIE_DOMAIN': '.thing.com',
        }
    }


def test_cookie_notice(settings):
    settings.PRIVACY_COOKIE_DOMAIN = '.thing.com'

    actual = context_processors.cookie_notice(None)

    assert actual == {
        'directory_components_cookie_notice': {
            'PRIVACY_COOKIE_DOMAIN': '.thing.com',
        }
    }


@pytest.fixture
def sso_user():
    return Mock(
        id=1,
        email='jim@example.com'
    )


@pytest.fixture
def request_logged_in(rf, sso_user):
    request = rf.get('/')
    request.sso_user = sso_user
    return request


@pytest.fixture
def request_logged_out(rf):
    request = rf.get('/')
    request.sso_user = None
    return request


def test_sso_logged_in(request_logged_in):
    context = context_processors.sso_processor(request_logged_in)
    assert context['sso_is_logged_in'] is True


def test_sso_profile_url(request_logged_in, settings):
    settings.SSO_PROFILE_URL = 'http://www.example.com/profile/'
    context = context_processors.sso_processor(request_logged_in)
    assert context['sso_profile_url'] == settings.SSO_PROFILE_URL


def test_sso_register_url_url(request_logged_in, settings):
    settings.SSO_PROXY_SIGNUP_URL = 'http://www.example.com/signup/'
    context = context_processors.sso_processor(request_logged_in)
    assert context['sso_register_url'] == (
        'http://www.example.com/signup/?next=http://testserver/'
    )


def test_sso_logged_out(request_logged_out):
    context = context_processors.sso_processor(request_logged_out)
    assert context['sso_is_logged_in'] is False


def test_sso_login_url(request_logged_in, settings):
    settings.SSO_PROXY_LOGIN_URL = 'http://www.example.com/login/'
    expected = 'http://www.example.com/login/?next=http://testserver/'
    context = context_processors.sso_processor(request_logged_in)
    assert context['sso_login_url'] == expected


def test_sso_logout_url(request_logged_in, settings):
    settings.SSO_PROXY_LOGOUT_URL = 'http://www.example.com/logout/'
    context = context_processors.sso_processor(request_logged_in)
    assert context['sso_logout_url'] == (
        'http://www.example.com/logout/?next=http://testserver/'
    )


def test_sso_user(request_logged_in, sso_user):
    context = context_processors.sso_processor(request_logged_in)
    assert context['sso_user'] == sso_user


def test_header_footer_processor(settings):
    context = context_processors.header_footer_processor(None)
    assert context['header_footer_urls'] == {
        'about': 'https://exred.com/about/',
        'business_planning': 'https://exred.com/business-planning/',
        'custom': 'https://exred.com/custom/',
        'customer_insight': 'https://exred.com/customer-insight/',
        'dit': urls.DIT,
        'exporting_new': 'https://exred.com/new',
        'exporting_occasional': 'https://exred.com/occasional/',
        'exporting_regular': 'https://exred.com/regular/',
        'finance': 'https://exred.com/finance/',
        'get_finance': 'https://exred.com/get-finance/',
        'getting_paid': 'https://exred.com/getting-paid/',
        'market_research': 'https://exred.com/market-research/',
        'operations_and_compliance': (
            'https://exred.com/operations-and-compliance/'
        ),
        'performance': 'https://exred.com/performance-dashboard/',
        'privacy_and_cookies': 'https://exred.com/privacy-and-cookies/',
        'terms_and_conditions': 'https://exred.com/terms-and-conditions/',
    }


def test_invest_header_footer_processor(settings):
    settings.HEADER_FOOTER_URLS_GREAT_HOME = 'http://home.com/'
    settings.INVEST_BASE_URL = 'http://invest.com/'

    context = context_processors.invest_header_footer_processor(None)
    assert context['invest_header_footer_urls'] == {
        'industries': 'https://invest.com/industries',
        'uk_setup_guide': 'https://invest.com/uk-setup-guide/',
    }


def test_urls_processor(settings):

    context = context_processors.urls_processor(None)

    assert context['directory_components_urls'] == {
        'contact_us': 'https://contact.com',
        'events': 'https://events.com',
        'exopps': 'https://exopps.com',
        'exred': 'https://exred.com',
        'fab': 'https://fab.com',
        'fas': 'https://fas.com',
        'feedback': 'https://contact.com/directory/FeedbackForm',
        'invest': 'https://invest.com',
        'soo': 'https://soo.com',
        'sso': 'https://sso.com',
    }


def test_feature_returns_expected_features(settings):
    settings.FEATURE_FLAGS = {
        'COMPANIES_HOUSE_OAUTH2_ENABLED': True
    }

    actual = context_processors.feature_flags(None)

    assert actual == {
        'features': {
            'COMPANIES_HOUSE_OAUTH2_ENABLED': True,
        }
    }
