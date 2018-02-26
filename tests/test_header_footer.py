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
        **context_processors.header_footer_processor(None),
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
        **context_processors.header_footer_processor(None),
    }
    html = render_to_string(template_name, context)
    assert 'Sign in' in html
    assert context['sso_login_url'] in html
    assert 'Sign out' not in html
    assert context['sso_logout_url'] not in html


def test_urls_exist_in_header():
    template_name = 'directory_components/header.html'
    context = context_processors.header_footer_processor(None)

    html = render_to_string(template_name, context)
    header_footer_elements = context['header_footer_elements']

    assert header_footer_elements['home']['url'] in html
    assert header_footer_elements['custom']['url'] in html

    for link in header_footer_elements['export_readiness']['items']:
        assert link['url'] in html

    for link in header_footer_elements['guidance']['items']:
        assert link['url'] in html

    for link in header_footer_elements['services']['items']:
        assert link['url'] in html


def test_urls_exist_in_footer():
    template_name = 'directory_components/footer.html'
    context = context_processors.header_footer_processor(None)
    html = render_to_string(template_name, context)
    header_footer_elements = context['header_footer_elements']

    assert header_footer_elements['custom']['url'] in html

    for link in header_footer_elements['export_readiness']['items']:
        assert link['url'] in html
    for link in header_footer_elements['guidance']['items']:
        assert link['url'] in html
    for link in header_footer_elements['services']['items']:
        assert link['url'] in html


def test_ids_rendered_in_header():
    template_name = 'directory_components/header.html'
    context = context_processors.header_footer_processor(None)
    html = render_to_string(template_name, context)

    assert context['header_footer_elements']['register']['id'] in html
    assert context['header_footer_elements']['signin']['id'] in html
    assert context['header_footer_elements']['home']['id'] in html
    assert context['header_footer_elements']['custom']['id'] in html

    exred = context['header_footer_elements']['export_readiness']['items']
    for exp_id in exred:
        assert exp_id['id'] in html
    for exp_id in context['header_footer_elements']['guidance']['items']:
        assert exp_id['id'] in html
    for exp_id in context['header_footer_elements']['services']['items']:
        assert exp_id['id'] in html


def test_ids_rendered_in_footer():
    template_name = 'directory_components/footer.html'
    context = context_processors.header_footer_processor(None)
    html = render_to_string(template_name, context)

    assert context['header_footer_elements']['custom']['id'] in html

    exred = context['header_footer_elements']['export_readiness']['items']
    for exp_id in exred:
        assert exp_id['id'] in html
    for exp_id in context['header_footer_elements']['guidance']['items']:
        assert exp_id['id'] in html
    for exp_id in context['header_footer_elements']['services']['items']:
        assert exp_id['id'] in html
    for exp_id in context['header_footer_elements']['site_links']['items']:
        assert exp_id['id'] in html


def test_header_ids_match_urls_and_text(settings):
    settings.HEADER_FOOTER_URLS_GREAT_HOME = 'http://home.com/'
    settings.HEADER_FOOTER_URLS_FAB = 'http://fab.com/'
    settings.HEADER_FOOTER_URLS_SOO = 'http://soo.com/'
    settings.HEADER_FOOTER_URLS_EVENTS = 'http://events.com/'

    exp_elements = {
        "export_readiness": {
            "items": [
                {
                    "title": "I'm new to exporting",
                    "id": "export-readiness-new",
                    "url": "http://home.com/new/"
                },
                {
                    "title": "I export occasionally",
                    "id": "export-readiness-occasional",
                    "url": "http://home.com/occasional/"
                },
                {
                    "title": "I'm a regular exporter",
                    "id": "export-readiness-regular",
                    "url": "http://home.com/regular/"
                }
            ]
        },
        "guidance": {
            "items": [
                {
                    "title": "Market research",
                    "id": "guidance-market-research",
                    "url": "http://home.com/market-research/"
                },
                {
                    "title": "Customer insight",
                    "id": "guidance-customer-insight",
                    "url": "http://home.com/customer-insight/"
                },
                {
                    "title": "Finance",
                    "id": "guidance-finance",
                    "url": "http://home.com/finance/"
                },
                {
                    "title": "Business planning",
                    "id": "guidance-business-planning",
                    "url": "http://home.com/business-planning/"
                },
                {
                    "title": "Getting paid",
                    "id": "guidance-getting-paid",
                    "url": "http://home.com/getting-paid/"
                },
                {
                    "title": "Operations and compliance",
                    "id": "guidance-operations-and-compliance",
                    "url": (
                        "http://home.com/operations-and-compliance/")
                }
            ]
        },
        "services": {
            "items": [
                {
                    "id": "services-find-a-buyer",
                    "title": "Create an export profile",
                    "url": "http://fab.com/",
                    "description": (
                        "Get promoted internationally with a great.gov.uk "
                        "trade profile")
                },
                {
                    "id": "services-selling-online-overseas",
                    "title": "Sell online overseas",
                    "url": "http://soo.com/",
                    "description": (
                        "Find the right marketplace for your business "
                        "and access special offers for sellers")
                },
                {
                    "id": "services-export-opportunities",
                    "title": "Find export opportunities",
                    "url": "http://home.com/export-opportunities/",
                    "description": "Find and apply for overseas opportunities"
                },
                {
                    "id": "services-get-finance",
                    "title": "Get finance",
                    "url": "http://home.com/get-finance/",
                    "description": (
                        "Get the finance you "
                        "need to compete and grow")
                },
                {
                    "id": "services-events",
                    "title": "Find events and visits",
                    "url": "http://events.com/",
                    "description": (
                        "Attend events and see how visits by "
                        "ministers can support your trade deals")
                }
            ]
        }
    }

    template_name = 'directory_components/header.html'
    context = context_processors.header_footer_processor(None)

    html = render_to_string(template_name, context)
    soup = BeautifulSoup(html, 'html.parser')

    home_element = soup.find(id='header-home-link')
    assert home_element.attrs['href'] == 'http://home.com/'

    custom_element = soup.find(id='header-custom-page-link')
    assert custom_element.attrs['href'] == 'http://home.com/custom/'

    for exp_element in exp_elements['export_readiness']['items']:
        exp_id = "header-{}".format(exp_element['id'])
        element = soup.find(id=exp_id)
        assert element.attrs['href'] == exp_element['url']
        assert element.string == exp_element['title']


def test_footer_ids_match_urls_and_text(settings):
    settings.HEADER_FOOTER_URLS_GREAT_HOME = 'http://home.com/'
    settings.HEADER_FOOTER_URLS_FAB = 'http://fab.com/'
    settings.HEADER_FOOTER_URLS_SOO = 'http://soo.com/'
    settings.HEADER_FOOTER_URLS_EVENTS = 'http://events.com/'
    settings.HEADER_FOOTER_URLS_CONTACT_US = 'http://contact.com/'
    settings.HEADER_FOOTER_URLS_DIT = 'http://dit.com/'

    exp_elements = {
        "export_readiness": {
            "items": [
                {
                    "title": "I'm new to exporting",
                    "id": "export-readiness-new",
                    "url": "http://home.com/new/"
                },
                {
                    "title": "I export occasionally",
                    "id": "export-readiness-occasional",
                    "url": "http://home.com/occasional/"
                },
                {
                    "title": "I'm a regular exporter",
                    "id": "export-readiness-regular",
                    "url": "http://home.com/regular/"
                }
            ]
        },
        "guidance": {
            "items": [
                {
                    "title": "Market research",
                    "id": "guidance-market-research",
                    "url": "http://home.com/market-research/"
                },
                {
                    "title": "Customer insight",
                    "id": "guidance-customer-insight",
                    "url": "http://home.com/customer-insight/"
                },
                {
                    "title": "Finance",
                    "id": "guidance-finance",
                    "url": "http://home.com/finance/"
                },
                {
                    "title": "Business planning",
                    "id": "guidance-business-planning",
                    "url": "http://home.com/business-planning/"
                },
                {
                    "title": "Getting paid",
                    "id": "guidance-getting-paid",
                    "url": "http://home.com/getting-paid/"
                },
                {
                    "title": "Operations and compliance",
                    "id": "guidance-operations-and-compliance",
                    "url": (
                        "http://home.com/operations-and-compliance/")
                }
            ]
        },
        "services": {
            "items": [
                {
                    "id": "services-find-a-buyer",
                    "title": "Create an export profile",
                    "url": "http://fab.com/",
                    "description": (
                        "Get promoted internationally with a great.gov.uk "
                        "trade profile")
                },
                {
                    "id": "services-selling-online-overseas",
                    "title": "Sell online overseas",
                    "url": "http://soo.com/",
                    "description": (
                        "Find the right marketplace for your business "
                        "and access special offers for sellers")
                },
                {
                    "id": "services-export-opportunities",
                    "title": "Find export opportunities",
                    "url": "http://home.com/export-opportunities/",
                    "description": "Find and apply for overseas opportunities"
                },
                {
                    "id": "services-get-finance",
                    "title": "Get finance",
                    "url": "http://home.com/get-finance/",
                    "description": (
                        "Get the finance you "
                        "need to compete and grow")
                },
                {
                    "id": "services-events",
                    "title": "Find events and visits",
                    "url": "http://events.com/",
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
                    "url": "http://home.com/about/"
                },
                {
                    "id": "site-links-contact",
                    "title": "Contact us",
                    "url": "http://contact.com/",
                },
                {
                    "id": "site-links-privacy-and-cookies",
                    "title": "Privacy and cookies",
                    "url": "http://home.com/privacy-and-cookies/",
                },
                {
                    "id": "site-links-t-and-c",
                    "title": "Terms and conditions",
                    "url": "http://home.com/terms-and-conditions/",
                },
                {
                    "id": "site-links-dit",
                    "title": "Department for International Trade on GOV.UK",
                    "url": "http://dit.com/",
                }
            ]
        }
    }

    template_name = 'directory_components/footer.html'
    context = context_processors.header_footer_processor(None)

    html = render_to_string(template_name, context)
    soup = BeautifulSoup(html, 'html.parser')

    custom_element = soup.find(id='footer-custom-page-link')
    assert custom_element.attrs['href'] == 'http://home.com/custom/'

    for exp_element in exp_elements['export_readiness']['items']:
        exp_id = "footer-{}".format(exp_element['id'])
        element = soup.find(id=exp_id)
        assert element.attrs['href'] == exp_element['url']
        assert element.string == exp_element['title']
