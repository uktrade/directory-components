from django.template.loader import render_to_string
from directory_components.context_processors import urls_processor


def test_google_tag_manager_project_id():
    context = {
        'directory_components_analytics': {
            'GOOGLE_TAG_MANAGER_ID': '123456',
        }
    }
    head_html = render_to_string(
        'directory_components/google_tag_manager_head.html', context
    )
    body_html = render_to_string(
        'directory_components/google_tag_manager_body.html', context
    )

    assert '123456' in head_html
    assert 'https://www.googletagmanager.com/ns.html?id=123456' in body_html


def test_google_tag_manager():
    expected_head = render_to_string(
        'directory_components/google_tag_manager_head.html', {}
    )
    expected_body = render_to_string(
        'directory_components/google_tag_manager_body.html', {}
    )

    html = render_to_string('directory_components/base.html', {})

    assert expected_head in html
    assert expected_body in html
    # sanity check
    assert 'www.googletagmanager.com' in expected_head
    assert 'www.googletagmanager.com' in expected_body


def test_google_tag_manager_env():

    context = {
        'directory_components_analytics': {
            'GOOGLE_TAG_MANAGER_ID': '123456',
            'GOOGLE_TAG_MANAGER_ENV': '&gtm_auth=hello'
        }
    }
    head_html = render_to_string(
        'directory_components/google_tag_manager_head.html', context
    )
    body_html = render_to_string(
        'directory_components/google_tag_manager_body.html', context
    )

    assert '&gtm_auth=hello' in head_html
    assert '&gtm_auth=hello' in body_html


def test_404_links(settings):
    """Test 404 page has links to home and contact-us."""
    settings.HEADER_FOOTER_URLS_GREAT_HOME = 'http://home.com'
    settings.HEADER_FOOTER_URLS_CONTACT_US = 'http://contact.com'
    context = urls_processor(None)
    html = render_to_string('directory_components/404.html', context)

    assert 'http://home.com' in html
    assert 'http://contact.com' in html


def test_404_content(settings):
    """Test 404 page has correct content."""
    context = urls_processor(None)
    html = render_to_string('directory_components/404.html', context)

    assert 'If you entered a web address please check it’s correct.' in html
