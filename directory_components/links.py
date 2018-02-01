from django.conf import settings
import os
import yaml


default_urls = {
  "GREAT_HOME": "https://great.gov.uk/",

  "CUSTOM_PAGE": "https://great.gov.uk/custom/",
  "EXPORTING_NEW": "https://great.gov.uk/new/",
  "EXPORTING_OCCASIONAL": "https://great.gov.uk/occasional/",
  "EXPORTING_REGULAR": "https://great.gov.uk/regular/",

  "GUIDANCE_MARKET_RESEARCH": "https://great.gov.uk/market-research/",
  "GUIDANCE_CUSTOMER_INSIGHT": "https://great.gov.uk/customer-insight/",
  "GUIDANCE_FINANCE": "https://great.gov.uk/finance/",
  "GUIDANCE_BUSINESS_PLANNING": "https://great.gov.uk/business-planning/",
  "GUIDANCE_GETTING_PAID": "https://great.gov.uk/getting-paid/",
  "GUIDANCE_OPERATIONS_AND_COMPLIANCE": (
    "https://great.gov.uk/operations-and-compliance/"),

  "SERVICES_FAB": "https://find-a-buyer.export.great.gov.uk/",
  "SERVICES_SOO": "https://selling-online-overseas.export.great.gov.uk/",
  "SERVICES_EXOPPS": "https://opportunities.export.great.gov.uk/",
  "SERVICES_GET_FINANCE": "https://great.gov.uk/get-finance/",
  "SERVICES_EVENTS": "https://events.trade.gov.uk/",

  "INFO_ABOUT": "https://great.gov.uk/about/",
  "INFO_CONTACT": "https://contact-us.export.great.gov.uk/directory/",
  "INFO_PRIVACY_AND_COOKIES": "https://great.gov.uk/privacy-and-cookies/",
  "INFO_TERMS_AND_CONDITIONS": "https://great.gov.uk/terms-and-conditions/",
  "INFO_DIT": (
    "https://www.gov.uk/government/organisations/"
    "department-for-international-trade/"),
}


def get_url(url_name):
    return getattr(settings, url_name, None) or (default_urls[url_name])


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
            "Get promoted internationally with a great.gov.uk trade profile")
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
  "site_links": [
    {
      "id": "site-links-about",
      "title": "About",
      "url": get_url("INFO_ABOUT")
      },
    {
      "id": "site-links-contact",
      "title": "Contact us",
      "url": get_url("INFO_CONTACT"),
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
    ]
}
