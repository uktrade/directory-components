from unittest.mock import Mock
import pytest

from directory_components import context_processors
import directory_components.urls as default_urls


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


def test_urls_processor(rf, settings):
    settings.GREAT_HOME = 'http://home.com'
    settings.CUSTOM_PAGE = 'http://custom.com'
    settings.EXPORTING_NEW = 'http://export.com/new'
    settings.EXPORTING_OCCASIONAL = 'http://export.com/occasional'
    settings.EXPORTING_REGULAR = 'http://export.com/regular'
    settings.GUIDANCE_MARKET_RESEARCH = 'http://market-research.com'
    settings.GUIDANCE_CUSTOMER_INSIGHT = 'http://customer-insight.com'
    settings.GUIDANCE_FINANCE = 'http://finance.com'
    settings.GUIDANCE_BUSINESS_PLANNING = 'http://business-planning.com'
    settings.GUIDANCE_GETTING_PAID = 'http://getting-paid.com'
    settings.GUIDANCE_OPERATIONS_AND_COMPLIANCE = 'http://compliance.com'
    settings.SERVICES_FAB = 'http://fab.com'
    settings.SERVICES_SOO = 'http://soo.com'
    settings.SERVICES_EXOPPS = 'http://exopps.com'
    settings.SERVICES_GET_FINANCE = 'http://export.com/get-finance'
    settings.SERVICES_EVENTS = 'http://events.com'
    settings.INFO_ABOUT = 'http://about.com'
    settings.INFO_CONTACT_US = 'http://contact.com'
    settings.INFO_PRIVACY_AND_COOKIES = 'http://privacy-and-cookies.com'
    settings.INFO_TERMS_AND_CONDITIONS = 'http://terms-and-conditions.com'
    settings.INFO_DIT = 'http://dit.com'

    actual_urls = context_processors.urls_processor(
        None)['header_footer_links']
    assert actual_urls['home']['url'] == 'http://home.com'
    assert actual_urls['custom']['url'] == 'http://custom.com'
    exp_urls = {
        'export_readiness': [
            'http://export.com/new',
            'http://export.com/occasional',
            'http://export.com/regular'
            ],
        'guidance': [
            'http://market-research.com',
            'http://customer-insight.com',
            'http://finance.com',
            'http://business-planning.com',
            'http://getting-paid.com',
            'http://compliance.com'
            ],
        'services': [
            'http://fab.com',
            'http://soo.com',
            'http://exopps.com',
            'http://export.com/get-finance',
            'http://events.com'
            ],
        'site_links': [
            'http://about.com',
            'http://contact.com',
            'http://privacy-and-cookies.com',
            'http://terms-and-conditions.com',
            'http://dit.com'
            ]
        }
    sections = exp_urls.keys()
    for section in sections:
        for exp, actual in zip(
                exp_urls[section],
                actual_urls[section]['items']):
            assert exp == actual['url']


def test_urls_processor_defaults(rf, settings):
    exp_urls = {
        'export_readiness': [
            default_urls.EXPORTING_NEW,
            default_urls.EXPORTING_OCCASIONAL,
            default_urls.EXPORTING_REGULAR
            ],
        'guidance': [
            default_urls.GUIDANCE_MARKET_RESEARCH,
            default_urls.GUIDANCE_CUSTOMER_INSIGHT,
            default_urls.GUIDANCE_FINANCE,
            default_urls.GUIDANCE_BUSINESS_PLANNING,
            default_urls.GUIDANCE_GETTING_PAID,
            default_urls.GUIDANCE_OPERATIONS_AND_COMPLIANCE
            ],
        'services': [
            default_urls.SERVICES_FAB,
            default_urls.SERVICES_SOO,
            default_urls.SERVICES_EXOPPS,
            default_urls.SERVICES_GET_FINANCE,
            default_urls.SERVICES_EVENTS
            ],
        'site_links': [
            default_urls.INFO_ABOUT,
            default_urls.INFO_CONTACT_US,
            default_urls.INFO_PRIVACY_AND_COOKIES,
            default_urls.INFO_TERMS_AND_CONDITIONS,
            default_urls.INFO_DIT
            ]
        }
    actual_urls = context_processors.urls_processor(
        None)['header_footer_links']
    assert actual_urls['home']['url'] == default_urls.GREAT_HOME
    assert actual_urls['custom']['url'] == default_urls.CUSTOM_PAGE
    sections = exp_urls.keys()
    for section in sections:
        for exp, actual in zip(
                exp_urls[section],
                actual_urls[section]['items']):
            assert exp == actual['url']


def test_urls_processor_defaults_explicitly_none(rf, settings):
    settings.GREAT_HOME = None
    settings.EXPORTING_NEW = None
    settings.EXPORTING_OCCASIONAL = None
    settings.EXPORTING_REGULAR = None
    settings.GUIDANCE_MARKET_RESEARCH = None
    settings.GUIDANCE_CUSTOMER_INSIGHT = None
    settings.GUIDANCE_BUSINESS_PLANNING = None
    settings.GUIDANCE_GETTING_PAID = None
    settings.GUIDANCE_OPERATIONS_AND_COMPLIANCE = None
    settings.SERVICES_FAB = None
    settings.SERVICES_SOO = None
    settings.SERVICES_EXOPPS = None
    settings.SERVICES_GET_FINANCE = None
    settings.SERVICES_EVENTS = None
    settings.INFO_ABOUT = None
    settings.INFO_CONTACT_US = None
    settings.INFO_PRIVACY_AND_COOKIES = None
    settings.INFO_TERMS_AND_CONDITIONS = None
    settings.INFO_DIT = None
    settings.CUSTOM_PAGE = None

    exp_urls = {
        'export_readiness': [
            default_urls.EXPORTING_NEW,
            default_urls.EXPORTING_OCCASIONAL,
            default_urls.EXPORTING_REGULAR
            ],
        'guidance': [
            default_urls.GUIDANCE_MARKET_RESEARCH,
            default_urls.GUIDANCE_CUSTOMER_INSIGHT,
            default_urls.GUIDANCE_FINANCE,
            default_urls.GUIDANCE_BUSINESS_PLANNING,
            default_urls.GUIDANCE_GETTING_PAID,
            default_urls.GUIDANCE_OPERATIONS_AND_COMPLIANCE
            ],
        'services': [
            default_urls.SERVICES_FAB,
            default_urls.SERVICES_SOO,
            default_urls.SERVICES_EXOPPS,
            default_urls.SERVICES_GET_FINANCE,
            default_urls.SERVICES_EVENTS
            ],
        'site_links': [
            default_urls.INFO_ABOUT,
            default_urls.INFO_CONTACT_US,
            default_urls.INFO_PRIVACY_AND_COOKIES,
            default_urls.INFO_TERMS_AND_CONDITIONS,
            default_urls.INFO_DIT
            ]
        }
    actual_urls = context_processors.urls_processor(
        None)['header_footer_links']
    assert actual_urls['home']['url'] == default_urls.GREAT_HOME
    assert actual_urls['custom']['url'] == default_urls.CUSTOM_PAGE
    sections = exp_urls.keys()
    for section in sections:
        for exp, actual in zip(
                exp_urls[section],
                actual_urls[section]['items']):
            assert exp == actual['url']
