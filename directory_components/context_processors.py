from django.conf import settings
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


def header_footer_processor(request):
    """Context processor specifically for the header and footer templates."""
    header_footer_elements = {
        "register": {
            "title": "Register",
            "id": "register-link"
        },
        "signin": {
            "title": "Sign in",
            "id": "sign-in-link"
        },
        "profile": {
            "title": "Profile",
            "id": "profile-link"
        },
        "signout": {
            "title": "Sign out",
            "id": "sign-out-link"
        },
        "home": {
            "title": "Home",
            "id": "home-link",
            "url": get_url("HEADER_FOOTER_URLS_GREAT_HOME")
        },
        "custom": {
            "title": "Your export journey",
            "id": "custom-page-link",
            "url": "{}custom/".format(get_url("HEADER_FOOTER_URLS_GREAT_HOME"))
        },
        "export_readiness": {
            "id": "export-readiness-links",
            "title": "Export readiness",
            "items": [
                {
                    "title": "I'm new to exporting",
                    "id": "export-readiness-new",
                    "url": "{}new/".format(get_url(
                        "HEADER_FOOTER_URLS_GREAT_HOME"))
                },
                {
                    "title": "I export occasionally",
                    "id": "export-readiness-occasional",
                    "url": "{}occasional/".format(get_url(
                        "HEADER_FOOTER_URLS_GREAT_HOME"))
                },
                {
                    "title": "I'm a regular exporter",
                    "id": "export-readiness-regular",
                    "url": "{}regular/".format(get_url(
                        "HEADER_FOOTER_URLS_GREAT_HOME"))
                }
            ]
        },
        "guidance": {
            "id": "guidance-links",
            "title": "Guidance",
            "items": [
                {
                    "title": "Market research",
                    "id": "guidance-market-research",
                    "url": "{}guidance/market-research/".format(
                        get_url("HEADER_FOOTER_URLS_GREAT_HOME"))
                },
                {
                    "title": "Customer insight",
                    "id": "guidance-customer-insight",
                    "url": "{}guidance/customer-insight/".format(
                        get_url("HEADER_FOOTER_URLS_GREAT_HOME"))
                },
                {
                    "title": "Finance",
                    "id": "guidance-finance",
                    "url": "{}guidance/finance/".format(
                        get_url("HEADER_FOOTER_URLS_GREAT_HOME"))
                },
                {
                    "title": "Business planning",
                    "id": "guidance-business-planning",
                    "url": "{}guidance/business-planning/".format(
                        get_url("HEADER_FOOTER_URLS_GREAT_HOME"))
                },
                {
                    "title": "Getting paid",
                    "id": "guidance-getting-paid",
                    "url": "{}guidance/getting-paid/".format(
                        get_url("HEADER_FOOTER_URLS_GREAT_HOME"))
                },
                {
                    "title": "Operations and compliance",
                    "id": "guidance-operations-and-compliance",
                    "url": "{}guidance/operations-and-compliance/".format(
                        get_url("HEADER_FOOTER_URLS_GREAT_HOME"))
                }
            ]
        },
        "services": {
            "id": "services-links",
            "title": "Services",
            "items": [
                {
                    "id": "services-find-a-buyer",
                    "title": "Create an export profile",
                    "url": get_url("HEADER_FOOTER_URLS_FAB"),
                    "description": (
                        "Get promoted internationally with a great.gov.uk "
                        "trade profile")
                },
                {
                    "id": "services-selling-online-overseas",
                    "title": "Sell online overseas",
                    "url": get_url("HEADER_FOOTER_URLS_SOO"),
                    "description": (
                        "Find the right marketplace for your business "
                        "and access special offers for sellers")
                },
                {
                    "id": "services-export-opportunities",
                    "title": "Find export opportunities",
                    "url": "{}export-opportunities/".format(
                        get_url("HEADER_FOOTER_URLS_GREAT_HOME")),
                    "description": "Find and apply for overseas opportunities"
                },
                {
                    "id": "services-get-finance",
                    "title": "Get finance",
                    "url": "{}get-finance/".format(
                        get_url("HEADER_FOOTER_URLS_GREAT_HOME")),
                    "description": (
                        "Get the finance you "
                        "need to compete and grow")
                },
                {
                    "id": "services-events",
                    "title": "Find events and visits",
                    "url": get_url("HEADER_FOOTER_URLS_EVENTS"),
                    "description": (
                        "Attend events and see how visits by "
                        "ministers can support your trade deals")
                }
            ]
        },
        "site_links": {
            "items": [
                {
                    "id": "site-links-about",
                    "title": "About",
                    "url": "{}about/".format(
                        get_url("HEADER_FOOTER_URLS_GREAT_HOME"))
                },
                {
                    "id": "site-links-contact",
                    "title": "Contact us",
                    "url": get_url("HEADER_FOOTER_URLS_CONTACT_US"),
                },
                {
                    "id": "site-links-privacy-and-cookies",
                    "title": "Privacy and cookies",
                    "url": "{}privacy-and-cookies/".format(
                        get_url("HEADER_FOOTER_URLS_GREAT_HOME"))
                },
                {
                    "id": "site-links-t-and-c",
                    "title": "Terms and conditions",
                    "url": "{}terms-and-conditions/".format(
                        get_url("HEADER_FOOTER_URLS_GREAT_HOME"))
                },
                {
                    "id": "site-links-dit",
                    "title": "Department for International Trade on GOV.UK",
                    "url": get_url("HEADER_FOOTER_URLS_DIT"),
                }
            ]
        }
    }
    return {
        'header_footer_elements': header_footer_elements
    }


def urls_processor(request):
    """For links to other services used outside of header/footer templates."""
    header_footer_urls = {
        "home": get_url("HEADER_FOOTER_URLS_GREAT_HOME"),
        "fab": get_url("HEADER_FOOTER_URLS_FAB"),
        "soo": get_url("HEADER_FOOTER_URLS_SOO"),
        "events": get_url("HEADER_FOOTER_URLS_EVENTS"),
        "contact_us": get_url("HEADER_FOOTER_URLS_CONTACT_US"),
        "dit": get_url("HEADER_FOOTER_URLS_DIT"),
    }
    return {
        'header_footer_urls': header_footer_urls
    }
