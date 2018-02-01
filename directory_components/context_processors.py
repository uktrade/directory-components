from django.conf import settings
from directory_components.helpers import add_next
from directory_components.links import header_footer_links


def sso_processor(request):
    url = request.build_absolute_uri()
    return {
        'sso_user': request.sso_user,
        'sso_is_logged_in': request.sso_user is not None,
        'sso_login_url': add_next(settings.SSO_PROXY_LOGIN_URL, url),
        'sso_register_url': add_next(settings.SSO_PROXY_SIGNUP_URL, url),
        'sso_logout_url': add_next(settings.SSO_PROXY_LOGOUT_URL, url),
        'sso_profile_url': settings.SSO_PROFILE_URL,
    }


def analytics(request):
    return {
        'directory_components_analytics': {
            'GOOGLE_TAG_MANAGER_ID': settings.GOOGLE_TAG_MANAGER_ID,
            'GOOGLE_TAG_MANAGER_ENV': settings.GOOGLE_TAG_MANAGER_ENV,
            'UTM_COOKIE_DOMAIN': settings.UTM_COOKIE_DOMAIN,
        }
    }


def header_footer_urls(request):
    return {
        'header_footer_links': header_footer_links
    }
