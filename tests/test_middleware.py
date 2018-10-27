from unittest.mock import Mock

import pytest

from django.http import HttpResponse
from django.urls import set_urlconf

from directory_components import middleware


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


def xtest_prefix_url_middleware_feature_off(rf, settings):
    settings.FEATURE_URL_PREFIX_ENABLED = False

    request = rf.get('/')

    response = PrefixUrlMiddleware().process_request(request)

    assert response is None


def xtest_prefix_url_middleware_not_starts_with_url_unknown_url(rf, settings):
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
def test_prefix_url_middleware_not_starts_with_url_known_url(
    rf, settings, url, expected
):
    set_urlconf('tests.urls_prefixed')

    request = rf.get(url)

    response = PrefixUrlMiddleware().process_request(request)

    assert response.status_code == 302
    assert response.url == expected


@pytest.mark.parametrize('url,expected', (
    ('/some/path/', 'https://example.com/components/some/path/'),
    ('/some/path', 'https://example.com/components/some/path/'),
    ('/some/path/?a=b', 'https://example.com/components/some/path/?a=b'),
    ('/some/path?a=b', 'https://example.com/components/some/path/?a=b'),
))
def test_prefix_url_middleware_not_starts_with_url_known_url_domain_set(
    rf, settings, url, expected
):
    settings.URL_PREFIX_DOMAIN = 'https://example.com'
    set_urlconf('tests.urls_prefixed')

    request = rf.get(url)

    response = PrefixUrlMiddleware().process_request(request)

    assert response.status_code == 302
    assert response.url == expected
