from django.conf import settings
from django.shortcuts import redirect


class RobotsIndexControlHeaderMiddlware:
    def process_response(self, request, response):
        if settings.FEATURE_SEARCH_ENGINE_INDEXING_DISABLED:
            response['X-Robots-Tag'] = 'noindex'
        return response


class MaintenanceModeMiddleware:
    maintenance_url = 'https://sorry.great.gov.uk'

    def process_request(self, request):
        if settings.FEATURE_MAINTENANCE_MODE_ENABLED:
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
