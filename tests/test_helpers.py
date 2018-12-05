from unittest import mock

import pytest

from django.urls import reverse

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
    settings.REMOTE_IP_ADDRESS_RETRIEVER = constants.IP_RETRIEVER_NAME_IPWARE

    retriever = helpers.RemoteIPAddressRetriever()

    assert isinstance(retriever, helpers.IpwareRemoteIPAddressRetriver)


def test_remote_ip_address_retriver_other(settings):
    settings.REMOTE_IP_ADDRESS_RETRIEVER = 'hello there'

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

    retriever.get_ip_address(request) == '8.8.8.8'
