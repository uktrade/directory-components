from unittest import mock

import pytest

from django.urls import reverse
from django.conf import settings

from directory_constants.constants.choices import COUNTRY_CHOICES

from directory_components import constants, helpers


@pytest.mark.parametrize('target,expected', (
    ('example.com', 'example.com?next=next.com'),
    ('example.com?next=existing.com', 'example.com?next=existing.com'),
    ('example.com?a=b', 'example.com?a=b&next=next.com'),
    ('example.com?a=b&next=existing.com', 'example.com?a=b&next=existing.com'),
))
def test_add_next(target, expected):
    next_url = 'next.com'
    assert helpers.add_next(target, next_url) == expected


def test_build_social_links(rf):
    social_links_builder = helpers.SocialLinkBuilder(
        url='http://testserver/',
        page_title='Do research first',
        app_title='Export Readiness',
    )

    assert social_links_builder.links['twitter'] == (
        'https://twitter.com/intent/tweet'
        '?text=Export%20Readiness%20-%20Do%20research%20first%20'
        'http://testserver/'
    )
    assert social_links_builder.links['facebook'] == (
        'https://www.facebook.com/share.php?u=http://testserver/'
    )
    assert social_links_builder.links['linkedin'] == (
        'https://www.linkedin.com/shareArticle?mini=true&'
        'url=http://testserver/&'
        'title=Export%20Readiness%20-%20Do%20research%20first%20'
        '&source=LinkedIn'
    )
    assert social_links_builder.links['email'] == (
        'mailto:?body=http://testserver/'
        '&subject=Export%20Readiness%20-%20Do%20research%20first%20'
    )


def test_remote_ip_address_retriver_paas_default(settings):
    retriever = helpers.RemoteIPAddressRetriever()

    assert isinstance(retriever, helpers.GovukPaaSRemoteIPAddressRetriver)


def test_remote_ip_address_retriver_paas(settings):
    settings.IP_RESTRICTOR_REMOTE_IP_ADDRESS_RETRIEVER = (
        constants.IP_RETRIEVER_NAME_IPWARE
    )
    retriever = helpers.RemoteIPAddressRetriever()

    assert isinstance(retriever, helpers.IpwareRemoteIPAddressRetriver)


def test_remote_ip_address_retriver_other(settings):
    settings.IP_RESTRICTOR_REMOTE_IP_ADDRESS_RETRIEVER = 'hello there'

    with pytest.raises(NotImplementedError):
        helpers.RemoteIPAddressRetriever()


@mock.patch(
    'directory_components.helpers.get_client_ip',
    mock.Mock(return_value=('8.8.8.8', False))
)
def test_ipware_remote_ip_retriever_unroutable(rf):
    request = rf.get(reverse('robots'))
    retriever = helpers.IpwareRemoteIPAddressRetriver()

    with pytest.raises(LookupError):
        retriever.get_ip_address(request)


@mock.patch(
    'directory_components.helpers.get_client_ip',
    mock.Mock(return_value=(None, False))
)
def test_ipware_remote_ip_retriever_unknown_ip(rf):
    request = rf.get(reverse('robots'))
    retriever = helpers.IpwareRemoteIPAddressRetriver()

    with pytest.raises(LookupError):
        retriever.get_ip_address(request)


@mock.patch(
    'directory_components.helpers.get_client_ip',
    mock.Mock(return_value=('8.8.8.8', True))
)
def test_ipware_remote_ip_retriever_routable(rf):
    request = rf.get(reverse('robots'))
    retriever = helpers.IpwareRemoteIPAddressRetriver()

    assert retriever.get_ip_address(request) == '8.8.8.8'


def test_govuk_retriever_missing_header(rf):
    retriever = helpers.GovukPaaSRemoteIPAddressRetriver
    with pytest.raises(LookupError) as e:
        retriever.get_ip_address(rf.request())
    assert retriever.MESSAGE_MISSING_HEADER in str(e.value)


def test_govuk_retriever_one_ip_address(rf):
    retriever = helpers.GovukPaaSRemoteIPAddressRetriver
    request = rf.request(**{'HTTP_X_FORWARDED_FOR': '8.8.8.8'})
    with pytest.raises(LookupError) as e:
        retriever.get_ip_address(request)
    assert retriever.MESSAGE_INVALID_IP_COUNT in str(e.value)


def test_govuk_retriever_two_ip_address(rf):
    retriever = helpers.GovukPaaSRemoteIPAddressRetriver
    request = rf.request(**{'HTTP_X_FORWARDED_FOR': '8.8.8.8, 1.1.1.1'})
    ips = retriever.get_ip_address(request)
    assert isinstance(ips, tuple)
    assert ips.second == '8.8.8.8'
    assert ips.third is None


def test_govuk_retriever_three_ip_address(rf):
    retriever = helpers.GovukPaaSRemoteIPAddressRetriver
    request = rf.request(
        **{'HTTP_X_FORWARDED_FOR': '8.8.8.8, 1.1.1.1, 2.2.2.2'}
    )
    ips = retriever.get_ip_address(request)
    assert isinstance(ips, tuple)
    assert ips.second == '1.1.1.1'
    assert ips.third == '8.8.8.8'


@pytest.mark.parametrize('country_code,country_name', COUNTRY_CHOICES)
def test_get_country_from_querystring(country_code, country_name, rf):
    url = reverse('index')
    request = rf.get(url, {'country': country_code})

    actual = helpers.get_country_from_querystring(request)

    assert actual == country_code


def test_get_country_from_querystring_invalid_code(rf):
    url = reverse('index')
    request = rf.get(url, {'country': 'foo'})

    actual = helpers.get_country_from_querystring(request)

    assert not actual


@pytest.mark.parametrize('mock_get', (
    {'country': ''},
    {},
))
def test_get_cookie_when_no_querystring(mock_get, rf):
    settings.COUNTRY_COOKIE_NAME = 'country'
    url = reverse('index')
    request = rf.get(url, mock_get)
    request.COOKIES = {'country': 'GB'}
    actual = helpers.get_user_country(request)

    assert actual == 'GB'


@pytest.mark.parametrize('path,expected_prefix', (
    ('/', 'en-gb'),
    ('/ar/', 'ar'),
    ('/es/industries/', 'es'),
    ('/zh-hans/industries/', 'zh-hans'),
    ('/de/industries/aerospace/', 'de'),
    ('/fr/industries/automotive/', 'fr'),
))
def test_get_language_from_prefix(path, expected_prefix):
    prefix = helpers.get_language_from_prefix(path)
    assert prefix == expected_prefix
