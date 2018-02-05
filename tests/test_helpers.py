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
