import pytest

from directory_components import helpers


@pytest.mark.parametrize('target,expected', (
    ('example.com', 'example.com?next=next.com'),
    ('example.com?next=existing.com', 'example.com?next=existing.com'),
    ('example.com?a=b', 'example.com?a=b&next=next.com'),
    ('example.com?a=b&next=existing.com', 'example.com?a=b&next=existing.com'),
))
def test_add_next(target, expected):
    next_url = 'next.com'
    assert helpers.add_next(target, next_url) == expected


def test_build_twitter_link(rf):
    social_links_builder = helpers.SocialLinkBuilder(
        url='http://testserver/',
        page_title='Do research first',
        app_title='Export Readiness',
    )

    assert social_links_builder.links['twitter'] == (
        'https://twitter.com/intent/tweet'
        '?text=Export%20Readiness%20-%20Do%20research%20first%20'
        'http://testserver/'
    )
    assert social_links_builder.links['facebook'] == (
        'https://www.facebook.com/share.php?u=http://testserver/'
    )
    assert social_links_builder.links['linkedin'] == (
        'https://www.linkedin.com/shareArticle?mini=true&'
        'url=http://testserver/&'
        'title=Export%20Readiness%20-%20Do%20research%20first%20'
        '&source=LinkedIn'
    )
    assert social_links_builder.links['email'] == (
        'mailto:?body=http://testserver/'
        '&subject=Export%20Readiness%20-%20Do%20research%20first%20'
    )
