import abc

from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve
from django.urls.exceptions import Resolver404

from directory_components import helpers


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
            prefixer = helpers.UrlPrefixer(request=request, prefix=self.prefix)
            if not prefixer.is_path_prefixed:
                try:
                    resolve(prefixer.path)
                except Resolver404:
                    pass
                else:
                    return redirect(prefixer.full_path)
