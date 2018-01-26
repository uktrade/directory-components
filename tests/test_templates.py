from django.template.loader import render_to_string


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
