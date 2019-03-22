import abc
import logging
from ipaddress import ip_address, ip_network
import urllib.parse

import admin_ip_restrictor.middleware

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import resolve
from django.urls.exceptions import Resolver404

from directory_components import constants
from directory_components import helpers

logger = logging.getLogger(__name__)


class RobotsIndexControlHeaderMiddlware:
    def process_response(self, request, response):
        if settings.FEATURE_FLAGS['SEARCH_ENGINE_INDEXING_OFF']:
            response['X-Robots-Tag'] = 'noindex'
        return response


class MaintenanceModeMiddleware:
    maintenance_url = 'https://sorry.great.gov.uk'

    def process_request(self, request):
        if settings.FEATURE_FLAGS['MAINTENANCE_MODE_ON']:
            return redirect(self.maintenance_url)


class NoCacheMiddlware:
    """Tell the browser to not cache the pages.

    Information that should be kept private can be viewed by anyone
    with access to the files in the browser's cache directory.

    """

    def process_response(self, request, response):
        if getattr(request, 'sso_user', None):
            response['Cache-Control'] = 'no-store, no-cache'
        return response


class AbstractPrefixUrlMiddleware(abc.ABC):

    @property
    @abc.abstractmethod
    def prefix(self):
        return ''

    def process_request(self, request):
        if settings.FEATURE_URL_PREFIX_ENABLED:
            redirect_url = self.get_redirect_url(request)
            if redirect_url:
                return redirect(redirect_url)

    def get_redirect_url(self, request):
        prefixer = helpers.UrlPrefixer(request=request, prefix=self.prefix)
        path = None
        host = self.get_redirect_domain(request)
        if not prefixer.is_path_prefixed and is_path_resolvable(prefixer.path):
            path = prefixer.full_path
        if host and not path and is_path_resolvable(request.path):
            path = request.get_full_path(force_append_slash=True)
        if host and path:
            return urllib.parse.urljoin(host, path)
        elif path:
            return path

    @staticmethod
    def get_redirect_domain(request):
        if settings.URL_PREFIX_DOMAIN:
            if not request.get_raw_uri().startswith(
                    settings.URL_PREFIX_DOMAIN
            ):
                return settings.URL_PREFIX_DOMAIN


class IPRestrictorMiddleware(
    admin_ip_restrictor.middleware.AdminIPRestrictorMiddleware
):
    MESSAGE_UNABLE_TO_DETERMINE_IP_ADDRESS = 'Unable to determine remote IP'

    def get_ip(self, request):
        try:
            return helpers.RemoteIPAddressRetriever().get_ip_address(request)
        except LookupError:
            logger.exception(self.MESSAGE_UNABLE_TO_DETERMINE_IP_ADDRESS)
            raise Http404()

    def _is_blocked_multiple_addresses(self, ips):
        """Determine if two IP addresses should be considered blocked."""
        blocked = True
        ip_second_allowed = ips.second in self.allowed_admin_ips
        ip_third_allowed = ips.third in self.allowed_admin_ips

        if any((ip_second_allowed, ip_third_allowed)):
            blocked = False

        for allowed_range in self.allowed_admin_ip_ranges:
            network_range = ip_network(allowed_range)
            ip_second_in_range = ip_address(ips.second) in network_range
            ip_third_in_range = ip_address(
                ips.third
            ) in network_range if ips.third else None
            if any((ip_second_in_range, ip_third_in_range)):
                blocked = False

        return blocked

    def is_blocked(self, ip):
        if isinstance(ip, tuple):
            return self._is_blocked_multiple_addresses(ip)
        return super().is_blocked(ip)

    def process_view(self, request, *args, **kwargs):
        cookie = request.COOKIES.get('ip-restrict-signature')
        if cookie and helpers.is_skip_ip_check_signature_valid(cookie):
            return None
        return super().process_view(request, *args, **kwargs)


def is_path_resolvable(path):
    if not path.endswith('/'):
        path += '/'
    try:
        resolve(path)
    except Resolver404:
        return False
    else:
        return True


class CountryMiddleware:
    def process_request(self, request):
        country_code = helpers.get_country_from_querystring(request)
        if country_code:
            request.COUNTRY_CODE = country_code

    def process_response(self, request, response):
        """
        Shares config with the language cookie as they serve a similar purpose
        """

        if hasattr(request, 'COUNTRY_CODE'):
            response.set_cookie(
                key=constants.COUNTRY_COOKIE_NAME,
                value=request.COUNTRY_CODE,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN
            )
        return response
