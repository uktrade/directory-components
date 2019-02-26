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


def test_header_footer_processor_export_journey_off(settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False

    context = context_processors.header_footer_processor(None)

    assert context['header_footer_urls'] == {
        'create_an_export_plan': (
            'https://exred.com/advice/create-an-export-plan/'),
        'find_an_export_market': (
            'https://exred.com/advice/find-an-export-market/'),
        'define_route_to_market': (
            'https://exred.com/advice/define-route-to-market/'),
        'get_export_finance_and_funding': (
            'https://exred.com/advice/get-export-finance-and-funding/'),
        'manage_payment_for_export_orders': (
            'https://exred.com/advice/manage-payment-for-export-orders/'),
        'prepare_to_do_business_in_a_foreign_country': (
            'https://exred.com/'
            'advice/prepare-to-do-business-in-a-foreign-country/'),
        'manage_legal_and_ethical_compliance': (
            'https://exred.com/advice/manage-legal-and-ethical-compliance/'),
        'prepare_for_export_procedures_and_logistics': (
            'https://exred.com/'
            'advice/prepare-for-export-procedures-and-logistics/'),
        'about': 'https://exred.com/about/',
        'dit': urls.DIT,
        'get_finance': 'https://exred.com/get-finance/',
        'performance': 'https://exred.com/performance-dashboard/',
        'privacy_and_cookies': 'https://exred.com/privacy-and-cookies/',
        'terms_and_conditions': 'https://exred.com/terms-and-conditions/',
        'market_access': 'https://exred.com/report-trade-barrier/'
    }


def test_invest_header_footer_processor():
    context = context_processors.invest_header_footer_processor(None)
    assert context['invest_header_footer_urls'] == {
        'industries': 'https://invest.com/industries/',
        'uk_setup_guide': 'https://invest.com/uk-setup-guide/',
    }


def test_urls_processor(settings):

    context = context_processors.urls_processor(None)

    assert context['services_urls'] == {
        'contact_us': 'https://exred.com/contact/',
        'events': 'https://events.com',
        'exopps': 'https://exopps.com',
        'exred': 'https://exred.com',
        'fab': 'https://fab.com',
        'fas': 'https://fas.com',
        'feedback': 'https://exred.com/contact/feedback/',
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
