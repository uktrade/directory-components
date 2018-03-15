from unittest.mock import Mock
import pytest
from urllib.parse import urljoin
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


@pytest.fixture
def exp_default_urls():
    return {
        'export_readiness': [
            urljoin(default_urls.HEADER_FOOTER_URLS_GREAT_HOME, 'new/'),
            urljoin(default_urls.HEADER_FOOTER_URLS_GREAT_HOME, 'occasional/'),
            urljoin(default_urls.HEADER_FOOTER_URLS_GREAT_HOME, 'regular/'),
            ],
        'guidance': [
            urljoin(
                default_urls.HEADER_FOOTER_URLS_GREAT_HOME,
                'market-research/'),
            urljoin(
                default_urls.HEADER_FOOTER_URLS_GREAT_HOME,
                'customer-insight/'),
            urljoin(
                default_urls.HEADER_FOOTER_URLS_GREAT_HOME,
                'finance/'),
            urljoin(
                default_urls.HEADER_FOOTER_URLS_GREAT_HOME,
                'business-planning/'),
            urljoin(
                default_urls.HEADER_FOOTER_URLS_GREAT_HOME,
                'getting-paid/'),
            urljoin(
                default_urls.HEADER_FOOTER_URLS_GREAT_HOME,
                'operations-and-compliance/'),
            ],
        'services': [
            default_urls.HEADER_FOOTER_URLS_FAB,
            default_urls.HEADER_FOOTER_URLS_SOO,
            urljoin(
                default_urls.HEADER_FOOTER_URLS_GREAT_HOME,
                'export-opportunities/'),
            urljoin(
                default_urls.HEADER_FOOTER_URLS_GREAT_HOME,
                'get-finance/'),
            default_urls.HEADER_FOOTER_URLS_EVENTS,
            ],
        'site_links': [
            urljoin(default_urls.HEADER_FOOTER_URLS_GREAT_HOME, 'about/'),
            default_urls.HEADER_FOOTER_URLS_CONTACT_US,
            urljoin(
                default_urls.HEADER_FOOTER_URLS_GREAT_HOME,
                'privacy-and-cookies/'),
            urljoin(
                default_urls.HEADER_FOOTER_URLS_GREAT_HOME,
                'terms-and-conditions/'),
            default_urls.HEADER_FOOTER_URLS_DIT,
            ]
        }


def test_header_footer_processor(settings):
    settings.HEADER_FOOTER_URLS_GREAT_HOME = 'http://home.com/'
    settings.HEADER_FOOTER_URLS_FAB = 'http://fab.com/'
    settings.HEADER_FOOTER_URLS_SOO = 'http://soo.com/'
    settings.HEADER_FOOTER_URLS_EVENTS = 'http://events.com/'
    settings.HEADER_FOOTER_URLS_CONTACT_US = 'http://contact.com/'
    settings.HEADER_FOOTER_URLS_DIT = 'http://dit.com/'

    actual_urls = context_processors.header_footer_processor(
        None)['header_footer_elements']
    assert actual_urls['home']['url'] == 'http://home.com/'
    assert actual_urls['custom']['url'] == 'http://home.com/custom/'
    exp_urls = {
        'export_readiness': [
            'http://home.com/new/',
            'http://home.com/occasional/',
            'http://home.com/regular/'
            ],
        'guidance': [
            'http://home.com/market-research/',
            'http://home.com/customer-insight/',
            'http://home.com/finance/',
            'http://home.com/business-planning/',
            'http://home.com/getting-paid/',
            'http://home.com/operations-and-compliance/'
            ],
        'services': [
            'http://fab.com/',
            'http://soo.com/',
            'http://home.com/export-opportunities/',
            'http://home.com/get-finance/',
            'http://events.com/'
            ],
        'site_links': [
            'http://home.com/about/',
            'http://contact.com/',
            'http://home.com/privacy-and-cookies/',
            'http://home.com/terms-and-conditions/',
            'http://dit.com/'
            ]
        }
    sections = exp_urls.keys()
    for section in sections:
        for exp, actual in zip(
                exp_urls[section],
                actual_urls[section]['items']):
            assert exp == actual['url']


def test_header_footer_processor_defaults(settings, exp_default_urls):
    actual_urls = context_processors.header_footer_processor(
        None)['header_footer_elements']

    exp_home = default_urls.HEADER_FOOTER_URLS_GREAT_HOME
    assert actual_urls['home']['url'] == exp_home
    assert actual_urls['custom']['url'] == urljoin(
        default_urls.HEADER_FOOTER_URLS_GREAT_HOME, 'custom/')

    sections = exp_default_urls.keys()
    for section in sections:
        for exp, actual in zip(
             exp_default_urls[section], actual_urls[section]['items']):
            assert exp == actual['url']


def test_header_footer_processor_defaults_explicitly_none(
     settings, exp_default_urls):
    settings.HEADER_FOOTER_URLS_GREAT_HOME = None
    settings.HEADER_FOOTER_URLS_FAB = None
    settings.HEADER_FOOTER_URLS_SOO = None
    settings.HEADER_FOOTER_URLS_EVENTS = None
    settings.INFO_CONTACT_US = None
    settings.INFO_DIT = None

    actual_urls = context_processors.header_footer_processor(
        None)['header_footer_elements']

    exp_home = default_urls.HEADER_FOOTER_URLS_GREAT_HOME
    exp_custom = urljoin(default_urls.HEADER_FOOTER_URLS_GREAT_HOME, 'custom/')
    assert actual_urls['home']['url'] == exp_home
    assert actual_urls['custom']['url'] == exp_custom
    sections = exp_default_urls.keys()
    for section in sections:
        for exp, actual in zip(
                exp_default_urls[section],
                actual_urls[section]['items']):
            assert exp == actual['url']


def test_urls_processor(settings):
    settings.HEADER_FOOTER_URLS_GREAT_HOME = 'http://home.com/'
    settings.HEADER_FOOTER_URLS_FAB = 'http://fab.com/'
    settings.HEADER_FOOTER_URLS_SOO = 'http://soo.com/'
    settings.HEADER_FOOTER_URLS_EVENTS = 'http://events.com/'
    settings.HEADER_FOOTER_URLS_CONTACT_US = 'http://contact.com/'
    settings.HEADER_FOOTER_URLS_DIT = 'http://dit.com/'

    actual_urls = context_processors.urls_processor(
        None)['directory_components_urls']

    exp_urls = {
        'home': 'http://home.com/',
        'fab': 'http://fab.com/',
        'soo': 'http://soo.com/',
        'events': 'http://events.com/',
        'contact_us': 'http://contact.com/',
        'dit': 'http://dit.com/',
    }

    for exp, actual in zip(exp_urls, actual_urls):
        assert exp == actual


def test_urls_processor_defaults(settings, exp_default_urls):
    actual_urls = context_processors.urls_processor(
        None)['directory_components_urls']

    exp_urls = {
        'home': default_urls.HEADER_FOOTER_URLS_GREAT_HOME,
        'fab': default_urls.HEADER_FOOTER_URLS_FAB,
        'soo': default_urls.HEADER_FOOTER_URLS_SOO,
        'events': default_urls.HEADER_FOOTER_URLS_EVENTS,
        'contact_us': default_urls.HEADER_FOOTER_URLS_CONTACT_US,
        'dit': default_urls.HEADER_FOOTER_URLS_DIT,
    }

    for exp, actual in zip(exp_urls, actual_urls):
        assert exp == actual


def test_urls_processor_defaults_explicitly_none(settings, exp_default_urls):
    settings.HEADER_FOOTER_URLS_GREAT_HOME = None
    settings.HEADER_FOOTER_URLS_FAB = None
    settings.HEADER_FOOTER_URLS_SOO = None
    settings.HEADER_FOOTER_URLS_EVENTS = None
    settings.INFO_CONTACT_US = None
    settings.INFO_DIT = None

    actual_urls = context_processors.urls_processor(
        None)['directory_components_urls']

    exp_urls = {
        'home': 'http://home.com/',
        'fab': 'http://fab.com/',
        'soo': 'http://soo.com/',
        'events': 'http://events.com/',
        'contact_us': 'http://contact.com/',
        'dit': 'http://dit.com/',
    }

    for exp, actual in zip(exp_urls, actual_urls):
        assert exp == actual
