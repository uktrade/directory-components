from django.template.loader import render_to_string
from bs4 import BeautifulSoup
import pytest
from directory_components import context_processors


@pytest.mark.parametrize('template_name', [
    'directory_components/header.html',
    'directory_components/footer.html',
    'directory_components/header_static.html',
])
def test_templates_rendered(template_name):
    html = render_to_string(template_name)
    assert "<div" in html
    assert "<ul" in html
    assert "<a" in html


def test_header_logged_in():
    template_name = 'directory_components/header.html'
    context = {
        'sso_is_logged_in': True,
        'sso_login_url': 'login.com',
        'sso_logout_url': 'logout.com',
        'header_footer_links': {
          'register': {
            'title': 'Register',
            'id': 'register-link'
            },
          'signin': {
            'title': 'Sign in',
            'id': 'sign-in-link'
            },
          'profile': {
            'title': 'Profile',
            'id': 'profile-link'
            },
          'signout': {
            'title': 'Sign out',
            'id': 'sign-out-link'
            }
        }
    }
    html = render_to_string(template_name, context)
    assert 'Sign in' not in html
    assert context['sso_login_url'] not in html
    assert 'Sign out' in html
    assert context['sso_logout_url'] in html


def test_header_logged_out():
    template_name = 'directory_components/header.html'
    context = {
        'sso_is_logged_in': False,
        'sso_login_url': 'login.com',
        'sso_logout_url': 'logout.com',
        'header_footer_links': {
          'register': {
            'title': 'Register',
            'id': 'register-link'
            },
          'signin': {
            'title': 'Sign in',
            'id': 'sign-in-link'
            },
          'profile': {
            'title': 'Profile',
            'id': 'profile-link'
            },
          'signout': {
            'title': 'Sign out',
            'id': 'sign-out-link'
            }
        }
    }
    html = render_to_string(template_name, context)
    assert 'Sign in' in html
    assert context['sso_login_url'] in html
    assert 'Sign out' not in html
    assert context['sso_logout_url'] not in html


def test_urls_exist_in_header():
    template_name = 'directory_components/header.html'
    context = {
        "header_footer_links": {
            "home": {"url": "http://home.com"},
            "custom": {"url": "http://custom.com"},
            "export_readiness": {
                "items": [
                    {"url": "http://new.com"},
                    {"url": "http://occasional.com"},
                    {"url": "http://regular.com"}
                    ]
            },
            "guidance": {
                "items": [
                    {"url": "http://market-research.com"},
                    {"url": "http://customer-insight.com"},
                    {"url": "http://finance.com"},
                    {"url": "http://business-planning.com"},
                    {"url": "http://getting-paid.com"},
                    {"url": "http://operations-and-compliance.com"}]
            },
            "services": {
                "items": [
                    {"url": "http://fab.com"},
                    {"url": "http://soo.com"},
                    {"url": "http://exopps.com"},
                    {"url": "http://get-finance.com"},
                    {"url": "http://events.com"}]
            }
        }
    }
    html = render_to_string(template_name, context)
    header_footer_links = context['header_footer_links']
    assert header_footer_links['home']['url'] in html
    assert header_footer_links['custom']['url'] in html
    for link in header_footer_links['export_readiness']['items']:
        assert link['url'] in html
    for link in header_footer_links['guidance']['items']:
        assert link['url'] in html
    for link in header_footer_links['services']['items']:
        assert link['url'] in html


def test_urls_exist_in_footer():
    template_name = 'directory_components/footer.html'
    context = {
        "header_footer_links": {
            "custom": {"url": "http://custom.com"},
            "export_readiness": {
                "items": [
                    {"url": "http://new.com"},
                    {"url": "http://occasional.com"},
                    {"url": "http://regular.com"}
                ]
            },
            "guidance": {
                "items": [
                    {"url": "http://market-research.com"},
                    {"url": "http://customer-insight.com"},
                    {"url": "http://finance.com"},
                    {"url": "http://business-planning.com"},
                    {"url": "http://getting-paid.com"},
                    {"url": "http://operations-and-compliance.com"}
                ]
            },
            "services": {
                "items": [
                    {"url": "http://fab.com"},
                    {"url": "http://soo.com"},
                    {"url": "http://exopps.com"},
                    {"url": "http://get-finance.com"},
                    {"url": "http://events.com"}
                ]
            },
            "site_links": {
                "items": [
                    {"url": "http://about.com"},
                    {"url": "http://contact.com"},
                    {"url": "http://privacy-and-cooki.es"},
                    {"url": "http://terms-andconditio.ns"},
                    {"url": "http://dit.com"}
                ]
            }
        }
    }
    html = render_to_string(template_name, context)
    header_footer_links = context['header_footer_links']
    assert header_footer_links['custom']['url'] in html
    for link in header_footer_links['export_readiness']['items']:
        assert link['url'] in html
    for link in header_footer_links['guidance']['items']:
        assert link['url'] in html
    for link in header_footer_links['services']['items']:
        assert link['url'] in html


def test_ids_rendered_in_header():
    template_name = 'directory_components/header.html'
    context = {
        "header_footer_links": {
            "register": {"id": "register-link"},
            "signin": {"id": "sign-in-link"},
            "home": {"id": "home-link"},
            "custom": {"id": "custom-page-link"},
            "export_readiness": {
                "id": "export-readiness-links",
                "items": [
                    {"id": "export-readiness-new"},
                    {"id": "export-readiness-occasional"},
                    {"id": "export-readiness-regular"}
                ]
            },
            "guidance": {
              "id": "guidance-links",
              "items": [
                    {"id": "guidance-market-research"},
                    {"id": "guidance-customer-insight"},
                    {"id": "guidance-finance"},
                    {"id": "guidance-business-planning"},
                    {"id": "guidance-getting-paid"},
                    {"id": "guidance-operations-and-compliance"}
                ]
              },
            "services": {
                "id": "services-links",
                "items": [
                    {"id": "services-find-a-buyer"},
                    {"id": "services-selling-online-overseas"},
                    {"id": "services-export-opportunities"},
                    {"id": "services-get-finance"},
                    {"id": "services-events"}
                ]
            }
        }
    }
    html = render_to_string(template_name, context)
    assert context['header_footer_links']['register']['id'] in html
    assert context['header_footer_links']['signin']['id'] in html
    assert context['header_footer_links']['home']['id'] in html
    assert context['header_footer_links']['custom']['id'] in html
    for exp_id in context['header_footer_links']['export_readiness']['items']:
        assert exp_id['id'] in html
    for exp_id in context['header_footer_links']['guidance']['items']:
        assert exp_id['id'] in html
    for exp_id in context['header_footer_links']['services']['items']:
        assert exp_id['id'] in html


def test_ids_rendered_in_footer():
    template_name = 'directory_components/footer.html'
    context = {
        "header_footer_links": {
            "custom": {"id": "custom-page-link"},
            "export_readiness": {
                "id": "export-readiness-links",
                "items": [
                    {"id": "export-readiness-new"},
                    {"id": "export-readiness-occasional"},
                    {"id": "export-readiness-regular"}
                ]
            },
            "guidance": {
              "id": "guidance-links",
              "items": [
                    {"id": "guidance-market-research"},
                    {"id": "guidance-customer-insight"},
                    {"id": "guidance-finance"},
                    {"id": "guidance-business-planning"},
                    {"id": "guidance-getting-paid"},
                    {"id": "guidance-operations-and-compliance"}
                ]
              },
            "services": {
                "id": "services-links",
                "items": [
                    {"id": "services-find-a-buyer"},
                    {"id": "services-selling-online-overseas"},
                    {"id": "services-export-opportunities"},
                    {"id": "services-get-finance"},
                    {"id": "services-events"}
                ]
            },
            "site_links": {
                "items": [
                    {"id": "site-links-about"},
                    {"id": "site-links-contact"},
                    {"id": "site-links-privacy-and-cookies"},
                    {"id": "site-links-t-and-c"},
                    {"id": "site-links-dit"}
                ]
            }
        }
    }
    html = render_to_string(template_name, context)
    assert context['header_footer_links']['custom']['id'] in html
    for exp_id in context['header_footer_links']['export_readiness']['items']:
        assert exp_id['id'] in html
    for exp_id in context['header_footer_links']['guidance']['items']:
        assert exp_id['id'] in html
    for exp_id in context['header_footer_links']['services']['items']:
        assert exp_id['id'] in html
    for exp_id in context['header_footer_links']['site_links']['items']:
        assert exp_id['id'] in html


def test_header_ids_match_urls_and_text(settings):
    settings.GREAT_HOME = 'http://home.com'
    settings.CUSTOM_PAGE = 'http://custom.com'
    settings.EXPORTING_NEW = 'http://export.com/new'
    settings.EXPORTING_OCCASIONAL = 'http://export.com/occasional'
    settings.EXPORTING_REGULAR = 'http://export.com/regular'
    settings.GUIDANCE_MARKET_RESEARCH = 'http://market-research.com'
    settings.GUIDANCE_CUSTOMER_INSIGHT = 'http://customer-insight.com'
    settings.GUIDANCE_FINANCE = 'http://finance.com'
    settings.GUIDANCE_BUSINESS_PLANNING = 'http://business-planning.com'
    settings.GUIDANCE_GETTING_PAID = 'http://getting-paid.com'
    settings.GUIDANCE_OPERATIONS_AND_COMPLIANCE = 'http://compliance.com'
    settings.SERVICES_FAB = 'http://fab.com'
    settings.SERVICES_SOO = 'http://soo.com'
    settings.SERVICES_EXOPPS = 'http://exopps.com'
    settings.SERVICES_GET_FINANCE = 'http://export.com/get-finance'
    settings.SERVICES_EVENTS = 'http://events.com'

    exp_elements = {
        "export_readiness": {
            "items": [
                {
                    "title": "I'm new to exporting",
                    "id": "export-readiness-new",
                    "url": "http://export.com/new"
                },
                {
                    "title": "I export occasionally",
                    "id": "export-readiness-occasional",
                    "url": "http://export.com/occasional"
                },
                {
                    "title": "I'm a regular exporter",
                    "id": "export-readiness-regular",
                    "url": "http://export.com/regular"
                }
            ]
        },
        "guidance": {
            "items": [
                {
                    "title": "Market research",
                    "id": "guidance-market-research",
                    "url": "http://market-research.com"
                },
                {
                    "title": "Customer insight",
                    "id": "guidance-customer-insight",
                    "url": "http://customer-insight.com"
                },
                {
                    "title": "Finance",
                    "id": "guidance-finance",
                    "url": "http://finance.com"
                },
                {
                    "title": "Business planning",
                    "id": "guidance-business-planning",
                    "url": "http://business-planning.com"
                },
                {
                    "title": "Getting paid",
                    "id": "guidance-getting-paid",
                    "url": "http://getting-paid.com"
                },
                {
                    "title": "Operations and compliance",
                    "id": "guidance-operations-and-compliance",
                    "url": "http://compliance.com"
                }
            ]
        },
        "services": {
            "items": [
                {
                    "id": "services-find-a-buyer",
                    "title": "Create an export profile",
                    "url": "http://fab.com",
                    "description": (
                        "Get promoted internationally with a great.gov.uk "
                        "trade profile")
                },
                {
                    "id": "services-selling-online-overseas",
                    "title": "Sell online overseas",
                    "url": "http://soo.com",
                    "description": (
                        "Find the right marketplace for your business "
                        "and access special offers for sellers")
                },
                {
                    "id": "services-export-opportunities",
                    "title": "Find export opportunities",
                    "url": "http://exopps.com",
                    "description": "Find and apply for overseas opportunities"
                },
                {
                    "id": "services-get-finance",
                    "title": "Get finance",
                    "url": "http://get-finance.com",
                    "description": (
                        "Get the finance you "
                        "need to compete and grow")
                },
                {
                    "id": "services-events",
                    "title": "Find events and visits",
                    "url": "http://events.com",
                    "description": (
                        "Attend events and see how visits by "
                        "ministers can support your trade deals")
                }
            ]
        }
    }

    template_name = 'directory_components/header.html'
    context = context_processors.urls_processor(None)

    html = render_to_string(template_name, context)
    soup = BeautifulSoup(html, 'html.parser')
    home_element = soup.find(id='header-home-link')
    assert home_element.attrs['href'] == 'http://home.com'
    custom_element = soup.find(id='header-custom-page-link')
    assert custom_element.attrs['href'] == 'http://custom.com'
    for exp_element in exp_elements['export_readiness']['items']:
        exp_id = "header-{}".format(exp_element['id'])
        element = soup.find(id=exp_id)
        assert element.attrs['href'] == exp_element['url']
        assert element.string == exp_element['title']


def test_footer_ids_match_urls_and_text(settings):
    settings.CUSTOM_PAGE = 'http://custom.com'
    settings.EXPORTING_NEW = 'http://export.com/new'
    settings.EXPORTING_OCCASIONAL = 'http://export.com/occasional'
    settings.EXPORTING_REGULAR = 'http://export.com/regular'
    settings.GUIDANCE_MARKET_RESEARCH = 'http://market-research.com'
    settings.GUIDANCE_CUSTOMER_INSIGHT = 'http://customer-insight.com'
    settings.GUIDANCE_FINANCE = 'http://finance.com'
    settings.GUIDANCE_BUSINESS_PLANNING = 'http://business-planning.com'
    settings.GUIDANCE_GETTING_PAID = 'http://getting-paid.com'
    settings.GUIDANCE_OPERATIONS_AND_COMPLIANCE = 'http://compliance.com'
    settings.SERVICES_FAB = 'http://fab.com'
    settings.SERVICES_SOO = 'http://soo.com'
    settings.SERVICES_EXOPPS = 'http://exopps.com'
    settings.SERVICES_GET_FINANCE = 'http://export.com/get-finance'
    settings.SERVICES_EVENTS = 'http://events.com'
    settings.INFO_ABOUT = 'http://about.com'
    settings.INFO_CONTACT_US = 'http://contact.com'
    settings.INFO_PRIVACY_AND_COOKIES = 'http://privacy-and-cookies.com'
    settings.INFO_TERMS_AND_CONDITIONS = 'http://terms-and-conditions.com'
    settings.INFO_DIT = 'http://dit.com'

    exp_elements = {
        "export_readiness": {
            "items": [
                {
                    "title": "I'm new to exporting",
                    "id": "export-readiness-new",
                    "url": "http://export.com/new"
                },
                {
                    "title": "I export occasionally",
                    "id": "export-readiness-occasional",
                    "url": "http://export.com/occasional"
                },
                {
                    "title": "I'm a regular exporter",
                    "id": "export-readiness-regular",
                    "url": "http://export.com/regular"
                }
            ]
        },
        "guidance": {
            "items": [
                {
                    "title": "Market research",
                    "id": "guidance-market-research",
                    "url": "http://market-research.com"
                },
                {
                    "title": "Customer insight",
                    "id": "guidance-customer-insight",
                    "url": "http://customer-insight.com"
                },
                {
                    "title": "Finance",
                    "id": "guidance-finance",
                    "url": "http://finance.com"
                },
                {
                    "title": "Business planning",
                    "id": "guidance-business-planning",
                    "url": "http://business-planning.com"
                },
                {
                    "title": "Getting paid",
                    "id": "guidance-getting-paid",
                    "url": "http://getting-paid.com"
                },
                {
                    "title": "Operations and compliance",
                    "id": "guidance-operations-and-compliance",
                    "url": "http://compliance.com"
                }
            ]
        },
        "services": {
            "items": [
                {
                    "id": "services-find-a-buyer",
                    "title": "Create an export profile",
                    "url": "http://fab.com",
                    "description": (
                        "Get promoted internationally with a great.gov.uk "
                        "trade profile")
                },
                {
                    "id": "services-selling-online-overseas",
                    "title": "Sell online overseas",
                    "url": "http://soo.com",
                    "description": (
                        "Find the right marketplace for your business "
                        "and access special offers for sellers")
                },
                {
                    "id": "services-export-opportunities",
                    "title": "Find export opportunities",
                    "url": "http://exopps.com",
                    "description": "Find and apply for overseas opportunities"
                },
                {
                    "id": "services-get-finance",
                    "title": "Get finance",
                    "url": "http://get-finance.com",
                    "description": (
                        "Get the finance you "
                        "need to compete and grow")
                },
                {
                    "id": "services-events",
                    "title": "Find events and visits",
                    "url": "http://events.com",
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
                    "url": "http://about.com"
                },
                {
                    "id": "site-links-contact",
                    "title": "Contact us",
                    "url": "http://contact.com",
                },
                {
                    "id": "site-links-privacy-and-cookies",
                    "title": "Privacy and cookies",
                    "url": "http://privacy-and-cookies.com",
                },
                {
                    "id": "site-links-t-and-c",
                    "title": "Terms and conditions",
                    "url": "http://terms-and-conditions.com",
                },
                {
                    "id": "site-links-dit",
                    "title": "Department for International Trade on GOV.UK",
                    "url": "http://dit.com",
                }
            ]
        }
    }

    template_name = 'directory_components/footer.html'
    context = context_processors.urls_processor(None)

    html = render_to_string(template_name, context)
    soup = BeautifulSoup(html, 'html.parser')
    custom_element = soup.find(id='footer-custom-page-link')
    assert custom_element.attrs['href'] == 'http://custom.com'
    for exp_element in exp_elements['export_readiness']['items']:
        exp_id = "footer-{}".format(exp_element['id'])
        element = soup.find(id=exp_id)
        assert element.attrs['href'] == exp_element['url']
        assert element.string == exp_element['title']
