from django.template.loader import render_to_string
import pytest


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
        'header_footer_links': {
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
        'header_footer_links': {
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
            },
            "site_links": {
                "items": [
                    {"url": "http://about.com"},
                    {"url": "http://contact.com"},
                    {"url": "http://privacy-and-cooki.es"},
                    {"url": "http://terms-andconditio.ns"},
                    {"url": "http://dit.com"}
                ]}
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
        'header_footer_links': {
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
        'header_footer_links': {
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
