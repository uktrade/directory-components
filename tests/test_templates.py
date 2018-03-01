from django.template.loader import render_to_string
from directory_components.context_processors import urls_processor
from directory_components.context_processors import header_footer_processor


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


def test_base_page_links(settings):
    settings.HEADER_FOOTER_URLS_CONTACT_US = 'http://contact.com'
    context = urls_processor(None)
    html = render_to_string('directory_components/base.html', context)

    assert 'http://contact.com' in html


def test_404_links(settings):
    """Test 404 page has links to home and contact-us."""
    settings.HEADER_FOOTER_URLS_GREAT_HOME = 'http://home.com'
    settings.HEADER_FOOTER_URLS_CONTACT_US = 'http://contact.com'
    context = urls_processor(None)
    html = render_to_string('404.html', context)

    assert 'http://home.com' in html
    assert 'http://contact.com' in html


def test_404_content(settings):
    """Test 404 page has correct content."""
    context = urls_processor(None)
    html = render_to_string('404.html', context)

    assert 'If you entered a web address please check it’s correct.' in html


def test_footer():
    template_name = 'directory_components/footer.html'
    context = header_footer_processor(None)
    html = render_to_string(template_name, context)
    exp_urls = [
        'https://great.gov.uk/custom/',
        'https://great.gov.uk/new/',
        'https://great.gov.uk/regular/',
        'https://great.gov.uk/occasional/',
        'https://great.gov.uk/market-research/',
        'https://great.gov.uk/customer-insight/',
        'https://great.gov.uk/finance/',
        'https://great.gov.uk/business-planning/',
        'https://great.gov.uk/getting-paid/',
        'https://great.gov.uk/operations-and-compliance/',
        'https://find-a-buyer.export.great.gov.uk/',
        'https://selling-online-overseas.export.great.gov.uk/',
        'https://contact-us.export.great.gov.uk/directory/',
        ('https://www.gov.uk/government/organisations/'
            'department-for-international-trade/')
    ]
    for url in exp_urls:
        assert url in html
