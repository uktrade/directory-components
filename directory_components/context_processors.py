from urllib.parse import urljoin

from django.conf import settings
from django.utils.functional import lazy

from directory_components.helpers import add_next
import directory_components.urls as default_urls


def get_url(url_name):
    return getattr(settings, url_name, None) or getattr(default_urls, url_name)


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


def cookie_notice(request):
    return {
        'directory_components_cookie_notice': {
            'PRIVACY_COOKIE_DOMAIN': settings.PRIVACY_COOKIE_DOMAIN
        }
    }


@lazy
def lazy_build_url(url_name, path):
    return urljoin(get_url(url_name), path)


TERMS_AND_CONDITIONS_URL = lazy_build_url(
    'HEADER_FOOTER_URLS_GREAT_HOME',
    'terms-and-conditions/'
)

PRIVACY_URL = lazy_build_url(
    'HEADER_FOOTER_URLS_GREAT_HOME',
    'privacy-and-cookies/'
)

PERFORMANCE_URL = lazy_build_url(
    'HEADER_FOOTER_URLS_GREAT_HOME',
    'performance-dashboard/'
)


def header_footer_processor(request):
    """Context processor specifically for the header and footer templates."""
    header_footer_urls = {
        'home': get_url('HEADER_FOOTER_URLS_GREAT_HOME'),
        'custom': lazy_build_url(
            'HEADER_FOOTER_URLS_GREAT_HOME',
            'custom/'),
        'exporting_new': lazy_build_url(
            'HEADER_FOOTER_URLS_GREAT_HOME',
            'new/'),
        'exporting_occasional': lazy_build_url(
            'HEADER_FOOTER_URLS_GREAT_HOME',
            'occasional/'),
        'exporting_regular': lazy_build_url(
            'HEADER_FOOTER_URLS_GREAT_HOME',
            'regular/'),
        'market_research': lazy_build_url(
            'HEADER_FOOTER_URLS_GREAT_HOME',
            'market-research/'),
        'customer_insight': lazy_build_url(
            'HEADER_FOOTER_URLS_GREAT_HOME',
            'customer-insight/'),
        'finance': lazy_build_url(
            'HEADER_FOOTER_URLS_GREAT_HOME',
            'finance/'),
        'business_planning': lazy_build_url(
            'HEADER_FOOTER_URLS_GREAT_HOME',
            'business-planning/'),
        'getting_paid': lazy_build_url(
            'HEADER_FOOTER_URLS_GREAT_HOME',
            'getting-paid/'),
        'operations_and_compliance': lazy_build_url(
            'HEADER_FOOTER_URLS_GREAT_HOME',
            'operations-and-compliance/'),
        'exopps': lazy_build_url(
            'HEADER_FOOTER_URLS_GREAT_HOME',
            'export-opportunities/'),
        'get_finance': lazy_build_url(
            'HEADER_FOOTER_URLS_GREAT_HOME',
            'get-finance/'),
        'about': lazy_build_url(
            'HEADER_FOOTER_URLS_GREAT_HOME',
            'about/'),
        'privacy_and_cookies': PRIVACY_URL,
        'terms_and_conditions': TERMS_AND_CONDITIONS_URL,
        'performance': PERFORMANCE_URL,
        'fab': get_url('HEADER_FOOTER_URLS_FAB'),
        'soo': get_url('HEADER_FOOTER_URLS_SOO'),
        'events': get_url('HEADER_FOOTER_URLS_EVENTS'),
        'contact_us': get_url('HEADER_FOOTER_URLS_CONTACT_US'),
        'dit': get_url('HEADER_FOOTER_URLS_DIT'),
    }
    return {
        'header_footer_urls': header_footer_urls
    }


def invest_header_footer_processor(request):
    invest_header_footer_urls = {
        'home': get_url('INVEST_BASE_URL'),
        'industries': lazy_build_url(
            'INVEST_BASE_URL',
            'industries/'),
        'uk_setup_guide': lazy_build_url(
            'INVEST_BASE_URL',
            'uk-setup-guide/'),
        'contact_us': lazy_build_url(
            'INVEST_BASE_URL',
            'contact/'),
        'part_of_great': get_url('HEADER_FOOTER_URLS_GREAT_HOME'),
        'privacy_and_cookies': PRIVACY_URL,
        'terms_and_conditions': TERMS_AND_CONDITIONS_URL,
    }
    return {
        'invest_header_footer_urls': invest_header_footer_urls
    }


def urls_processor(request):
    """For links to other services used outside of header/footer templates."""
    directory_components_urls = {
        "home": get_url("HEADER_FOOTER_URLS_GREAT_HOME"),
        "fab": get_url("HEADER_FOOTER_URLS_FAB"),
        "fas": get_url("COMPONENTS_URLS_FAS"),
        "soo": get_url("HEADER_FOOTER_URLS_SOO"),
        "events": get_url("HEADER_FOOTER_URLS_EVENTS"),
        "contact_us": get_url("HEADER_FOOTER_URLS_CONTACT_US"),
        "dit": get_url("HEADER_FOOTER_URLS_DIT"),
        "terms": TERMS_AND_CONDITIONS_URL,
        "privacy": PRIVACY_URL,
        "performance": PERFORMANCE_URL,
    }
    return {
        'directory_components_urls': directory_components_urls
    }


def feature_flags(request):
    return {
        'features': settings.FEATURE_FLAGS
    }
