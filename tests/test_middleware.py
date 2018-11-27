from unittest.mock import Mock

from mohawk import Sender
import pytest

from django.http import HttpResponse
from django.urls import reverse, set_urlconf

from directory_components import constants, middleware


class PrefixUrlMiddleware(middleware.AbstractPrefixUrlMiddleware):
    prefix = '/components/'


def test_robots_index_control_middlware_sso_user(rf):
    request = rf.get('/')
    request.sso_user = Mock()
    response = HttpResponse()

    response = (
        middleware.RobotsIndexControlHeaderMiddlware()
        .process_response(request, response)
    )

    assert response['X-Robots-Tag'] == 'noindex'


def test_maintenance_mode_middleware_feature_flag_on(rf, settings):
    settings.FEATURE_FLAGS['MAINTENANCE_MODE_ON'] = True
    request = rf.get('/')

    response = middleware.MaintenanceModeMiddleware().process_request(request)

    assert response.status_code == 302
    assert response.url == middleware.MaintenanceModeMiddleware.maintenance_url


def test_maintenance_mode_middleware_feature_flag_off(rf, settings):
    settings.FEATURE_FLAGS['MAINTENANCE_MODE_ON'] = False

    request = rf.get('/')

    response = middleware.MaintenanceModeMiddleware().process_request(request)

    assert response is None


def test_no_cache_middlware_sso_user(rf):
    request = rf.get('/')
    request.sso_user = Mock()
    response = HttpResponse()

    output = middleware.NoCacheMiddlware().process_response(request, response)

    assert output == response
    assert output['Cache-Control'] == 'no-store, no-cache'


def test_no_cache_middlware_anon_user(rf):
    request = rf.get('/')
    request.sso_user = None
    response = HttpResponse()

    output = middleware.NoCacheMiddlware().process_response(request, response)

    assert output == response
    assert 'Cache-Control' not in output


def test_no_cache_middleware_sso_user_not_in_request(rf):
    request = rf.get('/')
    response = HttpResponse()

    output = middleware.NoCacheMiddlware().process_response(request, response)

    assert output == response
    assert 'Cache-Control' not in output


def test_prefix_url_middleware_feature_off(rf, settings):
    settings.FEATURE_URL_PREFIX_ENABLED = False

    request = rf.get('/')

    response = PrefixUrlMiddleware().process_request(request)

    assert response is None


def test_prefix_url_middleware_unknown_url(rf, settings):
    settings.FEATURE_URL_PREFIX_ENABLED = True
    request = rf.get('/some-unknown-url/')

    response = PrefixUrlMiddleware().process_request(request)

    assert response is None


@pytest.mark.parametrize('url,expected', (
    ('/some/path/', '/components/some/path/'),
    ('/some/path', '/components/some/path/'),
    ('/some/path/?a=b', '/components/some/path/?a=b'),
    ('/some/path?a=b', '/components/some/path/?a=b'),
))
def test_prefix_url_middleware_starts_with_known_url(
    rf, settings, url, expected
):
    set_urlconf('tests.urls_prefixed')

    request = rf.get(url)

    response = PrefixUrlMiddleware().process_request(request)

    assert response.status_code == 302
    assert response.url == expected


@pytest.mark.parametrize('url,expected', (
    ('/some/path/', 'http://foo.com/components/some/path/'),
    ('/some/path', 'http://foo.com/components/some/path/'),
    ('/some/path/?a=b', 'http://foo.com/components/some/path/?a=b'),
    ('/some/path?a=b', 'http://foo.com/components/some/path/?a=b'),
))
def test_prefix_url_middleware_starts_with_known_url_domain_set(
    rf, settings, url, expected
):
    settings.URL_PREFIX_DOMAIN = 'http://foo.com'
    set_urlconf('tests.urls_prefixed')

    request = rf.get(url)

    response = PrefixUrlMiddleware().process_request(request)

    assert response.status_code == 302
    assert response.url == expected


def test_prefix_url_middleware_unknown_url_wrong_domain(rf, settings):
    settings.FEATURE_URL_PREFIX_ENABLED = True
    settings.URL_PREFIX_DOMAIN = 'http://foo.com'

    request = rf.get('/some-unknown-url/', HTTP_HOST='wrong.com')

    response = PrefixUrlMiddleware().process_request(request)

    assert response is None


@pytest.mark.parametrize('url,expected', (
    ('/some/path/', 'http://foo.com/components/some/path/'),
    ('/some/path', 'http://foo.com/components/some/path/'),
    ('/some/path/?a=b', 'http://foo.com/components/some/path/?a=b'),
    ('/some/path?a=b', 'http://foo.com/components/some/path/?a=b'),
    ('/components/some/path/', 'http://foo.com/components/some/path/'),
    ('/components/some/path', 'http://foo.com/components/some/path/'),
    ('/components/some/path/?a=b', 'http://foo.com/components/some/path/?a=b'),
    ('/components/some/path?a=b', 'http://foo.com/components/some/path/?a=b'),
))
def test_prefix_url_middleware_starts_with_known_url_wrong_domain(
    rf, settings, url, expected
):
    settings.URL_PREFIX_DOMAIN = 'http://foo.com'

    set_urlconf('tests.urls_prefixed')

    request = rf.get(url, HTTP_HOST='wrong.com')

    response = PrefixUrlMiddleware().process_request(request)

    assert response.status_code == 302
    assert response.url == expected


@pytest.mark.parametrize('url', (
    '/components/some/path/',
    '/components/some/path',
    '/components/some/path/?a=b',
    '/components/some/path?a=b',
))
def test_prefix_url_middleware_starts_with_known_url_correct_domain(
    rf, settings, url
):
    settings.URL_PREFIX_DOMAIN = 'http://foo.com'

    set_urlconf('tests.urls_prefixed')

    request = rf.get(url, HTTP_HOST='foo.com')

    response = PrefixUrlMiddleware().process_request(request)

    assert response is None


@pytest.mark.parametrize(
    'address_retriever,allowed_ips,get_kwargs',
    (
        # IPWARE should use REMOTE_ADDR
        (
            constants.IP_RETRIEVER_NAME_IPWARE,
            ['1.2.3.4'],
            dict(
                REMOTE_ADDR='8.8.8.8',
            ),
        ),
        # GOV_UK should not authorise using on REMOTE_ADDR
        (
            constants.IP_RETRIEVER_NAME_GOV_UK,
            ['1.2.3.4'],
            dict(
                REMOTE_ADDR='1.2.3.4',
            ),
        ),
        # GOV_UK should not authorise using last IP of X_FORWARDED_FOR
        (
            constants.IP_RETRIEVER_NAME_GOV_UK,
            ['1.2.3.4'],
            dict(
                HTTP_X_FORWARDED_FOR='8.8.8.8, 1.2.3.4',
            ),
        ),
        # GOV_UK should not authorise using first IP of X_FORWARDED_FOR
        (
            constants.IP_RETRIEVER_NAME_GOV_UK,
            ['1.2.3.4'],
            dict(
                HTTP_X_FORWARDED_FOR='1.2.3.4, 3.3.3.3, 8.8.8.8',
            ),
        ),
    ),
)
def test_if_not_from_authorized_ip_then_admin_404(
    address_retriever, allowed_ips, get_kwargs, settings, client
):
    settings.MIDDLEWARE_CLASSES = [
        'directory_components.middleware.IPRestrictorMiddleware'
    ]
    settings.REMOTE_IP_ADDRESS_RETRIEVER = address_retriever
    settings.ALLOWED_ADMIN_IPS = allowed_ips
    settings.RESTRICT_ADMIN = True
    response = client.get(reverse('admin:thing'), **get_kwargs)
    assert response.status_code == 404


@pytest.mark.parametrize(
    'address_retriever,allowed_ips,get_kwargs',
    (
        # IPWARE should authorise using REMOTE_ADDR
        (
            constants.IP_RETRIEVER_NAME_IPWARE,
            ['1.2.3.4'],
            dict(
                REMOTE_ADDR='1.2.3.4',
            ),
        ),
        # GOV_UK should authorise using on second-to-last IP of
        # X-Forwarded-For if there are two
        (
            constants.IP_RETRIEVER_NAME_GOV_UK,
            ['1.2.3.4'],
            dict(
                HTTP_X_FORWARDED_FOR='1.2.3.4, 8.8.8.8',
            ),
        ),
        # GOV_UK should authorise using second-to-last IP of
        # X-Forwarded-For if there are three
        (
            constants.IP_RETRIEVER_NAME_GOV_UK,
            ['1.2.3.4'],
            dict(
                HTTP_X_FORWARDED_FOR='5.4.3.2, 1.2.3.4, 8.8.8.8',
            ),
        ),
    ),
)
def test_if_from_authorized_ip_then_admin_302(
    address_retriever, allowed_ips, get_kwargs, settings, client
):
    settings.MIDDLEWARE_CLASSES = [
        'directory_components.middleware.IPRestrictorMiddleware'
    ]
    settings.REMOTE_IP_ADDRESS_RETRIEVER = address_retriever
    settings.ALLOWED_ADMIN_IPS = allowed_ips
    settings.RESTRICT_ADMIN = True
    response = client.get(reverse('admin:thing'), **get_kwargs)
    assert response.status_code == 302


# Test that non-admin URLs do not incorrectly give a 404, even if the IP is
# not authorised to perform admin
@pytest.mark.parametrize(
    'address_retriever,allowed_ips,get_kwargs',
    (
        (
            constants.IP_RETRIEVER_NAME_IPWARE,
            ['1.2.3.4'],
            dict(
                REMOTE_ADDR='8.8.8.8',
            ),
        ),
        (
            constants.IP_RETRIEVER_NAME_GOV_UK,
            ['1.2.3.4'],
            dict(
                HTTP_X_FORWARDED_FOR='8.8.8.8, 1.2.3.4',
            ),
        ),
        (
            constants.IP_RETRIEVER_NAME_GOV_UK,
            ['1.2.3.4'],
            dict(
                HTTP_X_FORWARDED_FOR='1.2.3.4, 3.3.3.3, 8.8.8.8',
            ),
        ),
    ),
)
def test_if_from_unauthorized_ip_then_non_admin_200(
    address_retriever, allowed_ips, get_kwargs, settings, client
):
    settings.MIDDLEWARE_CLASSES = [
        'directory_components.middleware.IPRestrictorMiddleware'
    ]
    settings.REMOTE_IP_ADDRESS_RETRIEVER = address_retriever
    settings.ALLOWED_ADMIN_IPS = allowed_ips
    settings.RESTRICT_ADMIN = True
    response = client.get(reverse('robots'), **get_kwargs)
    assert response.status_code == 200


def test_signature_check_skip_valid(
    client, settings
):
    settings.RESTRICT_ADMIN = True
    settings.REMOTE_IP_ADDRESS_RETRIEVER = constants.IP_RETRIEVER_NAME_IPWARE

    sender = Sender(
        {
            'id': settings.IP_RESTRICTOR_SKIP_CHECK_SENDER_ID,
            'key': settings.IP_RESTRICTOR_SKIP_CHECK_SECRET,
            'algorithm': 'sha256',
        },
        '/',
        '',
        always_hash_content=False
    )

    client.cookies['ip-restrict-signature'] = sender.request_header

    settings.MIDDLEWARE_CLASSES = [
        'directory_components.middleware.IPRestrictorMiddleware'
    ]
    response = client.get(reverse('robots'), REMOTE_ADDR='8.8.8.8')
    assert response.status_code == 200


def test_signature_check_skip_invalid(
    client, settings
):
    settings.RESTRICT_ADMIN = True
    settings.REMOTE_IP_ADDRESS_RETRIEVER = constants.IP_RETRIEVER_NAME_IPWARE
    settings.RESTRICTED_APP_NAMES = ['admin', '']

    client.cookies['ip-restrict-signature'] = '123'

    settings.MIDDLEWARE_CLASSES = [
        'directory_components.middleware.IPRestrictorMiddleware'
    ]
    response = client.get(reverse('robots'), REMOTE_ADDR='8.8.8.8')
    assert response.status_code == 404
