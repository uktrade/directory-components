import pytest

from django.template import Context, Template


def test_static_absolute(rf):
    template = Template(
        '{% load static_absolute from directory_components_tags %}'
        '{% static_absolute "directory_components/images/favicon.ico" %}'
    )

    context = Context({'request': rf.get('/')})
    html = template.render(context)

    assert html == (
        'http://testserver/static/directory_components/images/favicon.ico'
    )


def test_add_anchors():
    template = Template(
        '{% load add_anchors from directory_components_tags %}'
        '{{ html|add_anchors:"-section" }}'
    )

    context = Context({
        'html': '<br/><h2>Title one</h2><h2>Title two</h2><br/>'
    })
    html = template.render(context)

    assert html == (
        '<br/>'
        '<h2 id="title-one-section">Title one</h2>'
        '<h2 id="title-two-section">Title two</h2>'
        '<br/>'
    )


def test_add_anchors_no_suffix():
    template = Template(
        '{% load add_anchors from directory_components_tags %}'
        '{{ html|add_anchors }}'
    )

    context = Context({
        'html': '<br/><h2>Title one</h2><h2>Title two</h2><br/>'
    })
    html = template.render(context)

    assert html == (
        '<br/>'
        '<h2 id="title-one">Title one</h2>'
        '<h2 id="title-two">Title two</h2>'
        '<br/>'
    )


@pytest.mark.parametrize('input_html,expected_html', (
    ('<h1>content</h1>', '<h1 class="heading-xlarge">content</h1>'),
    ('<h2>content</h2>', '<h2 class="heading-large">content</h2>'),
    ('<h3>content</h3>', '<h3 class="heading-medium">content</h3>'),
    ('<h4>content</h4>', '<h4 class="heading-small">content</h4>'),
    ('<ul>content</ul>', '<ul class="list list-bullet">content</ul>'),
    ('<ol>content</ul>', '<ol class="list list-number">content</ol>'),
    ('<p>content</p>', '<p class="body-text">content</p>'),
    ('<a>content</a>', '<a class="link">content</a>'),
    ('<blockquote>a</blockquote>', '<blockquote class="quote">a</blockquote>')
))
def test_add_export_elements_classes(input_html, expected_html):
    template = Template(
        '{% load add_export_elements_classes from directory_components_tags %}'
        '{{ html|add_export_elements_classes }}'

    )
    context = Context({'html': input_html})

    html = template.render(context)
    assert html == expected_html
