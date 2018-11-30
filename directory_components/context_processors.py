from directory_constants.constants import urls

from django.conf import settings

from directory_components.helpers import add_next


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


def header_footer_processor(request):
    header_footer_urls = {
        'about': urls.ABOUT,
        'business_planning': urls.GUIDANCE_BUSINESS_PLANNING,
        'custom': urls.CUSTOM_PAGE,
        'customer_insight': urls.GUIDANCE_CUSTOMER_INSIGHT,
        'dit': urls.DIT,
        'exporting_new': urls.EXPORTING_NEW,
        'exporting_occasional': urls.EXPORTING_OCCASIONAL,
        'exporting_regular': urls.EXPORTING_REGULAR,
        'finance': urls.GUIDANCE_FINANCE,
        'get_finance': urls.GET_FINANCE,
        'getting_paid': urls.GUIDANCE_GETTING_PAID,
        'market_research': urls.GUIDANCE_MARKET_RESEARCH,
        'operations_and_compliance': urls.GUIDANCE_OPERATIONS_AND_COMPLIANCE,
        'performance': urls.PERFORMANCE_DASHBOARD,
        'privacy_and_cookies': urls.PRIVACY_AND_COOKIES,
        'terms_and_conditions': urls.TERMS_AND_CONDITIONS,
    }
    return {'header_footer_urls': header_footer_urls}


def invest_header_footer_processor(request):
    invest_header_footer_urls = {
        'industries': urls.INVEST_INDUSTRIES,
        'uk_setup_guide': urls.INVEST_SETUP_GUIDE,
    }
    return {'invest_header_footer_urls': invest_header_footer_urls}


def urls_processor(request):
    services_urls = {
        'contact_us': urls.CONTACT_US,
        'events': urls.SERVICES_EVENTS,
        'exopps': urls.SERVICES_EXOPPS,
        'exred': urls.SERVICE_EXPORT_READINESS,
        'fab': urls.SERVICES_FAB,
        'fas': urls.SERVICES_FAS,
        'feedback': urls.FEEDBACK,
        'invest': urls.SERVICES_INVEST,
        'soo': urls.SERVICES_SOO,
        'sso': urls.SERVICES_SSO,
    }
    return {'services_urls': services_urls}


def feature_flags(request):
    return {'features': settings.FEATURE_FLAGS}
