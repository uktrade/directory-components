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


def urls_processor(request):
    header_footer_links = {
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
        "url": get_url("GREAT_HOME")
        },
      "custom": {
        "title": "Your export journey",
        "id": "custom-page-link",
        "url": get_url("CUSTOM_PAGE")
        },
      "export_readiness": {
        "id": "export-readiness-links",
        "title": "Export readiness",
        "items": [
          {
            "title": "I'm new to exporting",
            "id": "export-readiness-new",
            "url": get_url("EXPORTING_NEW")
            },
          {
            "title": "I export occasionally",
            "id": "export-readiness-occasional",
            "url": get_url("EXPORTING_OCCASIONAL")
            },
          {
            "title": "I'm a regular exporter",
            "id": "export-readiness-regular",
            "url": get_url("EXPORTING_REGULAR")
            }]
        },
      "guidance": {
        "id": "guidance-links",
        "title": "Guidance",
        "items": [
          {
            "title": "Market research",
            "id": "guidance-market-research",
            "url": get_url("GUIDANCE_MARKET_RESEARCH")
            },
          {
            "title": "Customer insight",
            "id": "guidance-customer-insight",
            "url": get_url("GUIDANCE_CUSTOMER_INSIGHT")
            },
          {
            "title": "Finance",
            "id": "guidance-finance",
            "url": get_url("GUIDANCE_FINANCE")
            },
          {
            "title": "Business planning",
            "id": "guidance-business-planning",
            "url": get_url("GUIDANCE_BUSINESS_PLANNING")
            },
          {
            "title": "Getting paid",
            "id": "guidance-getting-paid",
            "url": get_url("GUIDANCE_GETTING_PAID")
            },
          {
            "title": "Operations and compliance",
            "id": "guidance-operations-and-compliance",
            "url": get_url("GUIDANCE_OPERATIONS_AND_COMPLIANCE")
            }]
        },
      "services": {
        "id": "services-links",
        "title": "Services",
        "items": [
          {
            "id": "services-find-a-buyer",
            "title": "Create an export profile",
            "url": get_url("SERVICES_FAB"),
            "description": (
                "Get promoted internationally with a great.gov.uk "
                "trade profile")
            },
          {
            "id": "services-selling-online-overseas",
            "title": "Sell online overseas",
            "url": get_url("SERVICES_SOO"),
            "description": (
                "Find the right marketplace for your business "
                "and access special offers for sellers")
            },
          {
            "id": "services-export-opportunities",
            "title": "Find export opportunities",
            "url": get_url("SERVICES_EXOPPS"),
            "description": "Find and apply for overseas opportunities"
            },
          {
            "id": "services-get-finance",
            "title": "Get finance",
            "url": get_url("SERVICES_GET_FINANCE"),
            "description": "Get the finance you need to compete and grow"
            },
          {
            "id": "services-events",
            "title": "Find events and visits",
            "url": get_url("SERVICES_EVENTS"),
            "description": (
                "Attend events and see how visits by "
                "ministers can support your trade deals")
            }]
        },
      "site_links": {
        "items": [
            {
              "id": "site-links-about",
              "title": "About",
              "url": get_url("INFO_ABOUT")
              },
            {
              "id": "site-links-contact",
              "title": "Contact us",
              "url": get_url("INFO_CONTACT_US"),
              },
            {
              "id": "site-links-privacy-and-cookies",
              "title": "Privacy and cookies",
              "url": get_url("INFO_PRIVACY_AND_COOKIES"),
              },
            {
              "id": "site-links-t-and-c",
              "title": "Terms and conditions",
              "url": get_url("INFO_TERMS_AND_CONDITIONS"),
              },
            {
              "id": "site-links-dit",
              "title": "Department for International Trade on GOV.UK",
              "url": get_url("INFO_DIT"),
              }
        ]}
    }
    return {
        'header_footer_links': header_footer_links
    }
