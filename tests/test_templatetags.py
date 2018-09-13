import pytest
from bs4 import BeautifulSoup

from django import forms
from django.template import Context, Template

from directory_components import fields

REQUIRED_MESSAGE = fields.PaddedCharField.default_error_messages['required']


class PaddedTestForm(forms.Form):
    field = fields.PaddedCharField(fillchar='0', max_length=6)


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


def test_render_form():
    form = PaddedTestForm(data={'field': 'value'})

    template = Template(
        '{% load render_form from directory_components_tags %}'
        '{% render_form form %}'
    )
    context = Context({'form': form})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    form_container = soup.find('div')
    assert 'form-group' in form_container['class']

    label = soup.find('label')
    assert 'form-label' in label['class']
    assert label['for'] == 'id_field'

    input_field = soup.find('input')
    assert input_field['id'] == 'id_field'


def test_card():
    card_content = {
        'title': 'title',
        'url': 'url',
        'description': 'description',
        'img_src': 'img_src',
        'img_alt': 'img_alt',
    }
    string = (
        "{{% load card from directory_components_tags %}}"
        "{{% card title='{title}' url='{url}' description='{description}' "
        "img_src='{img_src}' img_alt='{img_alt}' %}}"
        ).format(**card_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    card_link = soup.select('.card-link')[0]
    assert 'url' in card_link['href']

    card_image = soup.select('.card-image')[0]
    assert card_image['role'] == 'image'
    assert 'img_src' in card_image['style']
    assert card_image['aria-label'] == 'img_alt'
    assert card_image['title'] == 'img_alt'

    image_description = soup.select('p.visually-hidden')[0]
    assert image_description.string == 'img_alt'

    card_heading = soup.select('h3.heading-large')[0]
    assert card_heading.string == 'title'

    card_description = soup.select('p.description')[0]
    assert card_description.string == 'description'


def test_card_html():
    html_content = '<p>Test</p>'
    card_content = {
        'html_content': html_content,
    }
    string = (
        "{{% load card from directory_components_tags %}}"
        "{{% card html_content='{html_content}' %}}"
        ).format(**card_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)

    assert html_content in html


def test_labelled_card_with_image():
    card_content = {
        'title': 'title',
        'url': 'url',
        'description': 'description',
        'img_src': 'img_src',
        'img_alt': 'img_alt',
    }
    string = (
        "{{% load labelled_card from directory_components_tags %}}"
        "{{% labelled_card title='{title}' url='{url}' img_src='{img_src}' "
        "description='{description}' img_alt='{img_alt}' %}}"
        ).format(**card_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    card_link = soup.select('.labelled-card')[0]
    assert 'url' in card_link['href']

    card_inner = soup.select('div.card-inner')[0]
    assert 'with-image' in card_inner['class']

    card_image = soup.select('.card-image')[0]
    assert card_image['role'] == 'image'
    assert 'img_src' in card_image['style']
    assert card_image['aria-label'] == 'img_alt'
    assert card_image['title'] == 'img_alt'

    image_description = soup.select('p.visually-hidden')[0]
    assert image_description.string == 'img_alt'

    card_heading = soup.select('h3.title')[0]
    assert card_heading.string == 'title'

    card_description = soup.select('p.description')[0]
    assert card_description.string == 'description'


def test_labelled_card_without_image():
    card_content = {
        'title': 'title',
        'url': 'url',
        'description': 'description',
    }
    string = (
        "{{% load labelled_card from directory_components_tags %}}"
        "{{% labelled_card title='{title}' url='{url}' "
        "description='{description}' %}}"
        ).format(**card_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    card_inner = soup.select('div.card-inner')[0]
    assert 'with-image' not in card_inner['class']


def test_labelled_image_card():
    card_content = {
        'title': 'title',
        'url': 'url',
        'description': 'description',
        'img_src': 'img_src',
        'img_alt': 'img_alt',
    }
    string = (
        "{{% load labelled_image_card from directory_components_tags %}}"
        "{{% labelled_image_card title='{title}' url='{url}' "
        "img_src='{img_src}' "
        "description='{description}' img_alt='{img_alt}' %}}"
        ).format(**card_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')
    print(html)

    card_link = soup.select('.labelled-image-card')[0]
    assert 'url' in card_link['href']

    card_image = soup.select('.card-image')[0]
    assert card_image['role'] == 'image'
    assert 'img_src' in card_image['style']
    assert card_image['aria-label'] == 'img_alt'
    assert card_image['title'] == 'img_alt'

    image_description = soup.select('p.visually-hidden')[0]
    assert image_description.string == 'img_alt'

    card_heading = soup.select('h3.title')[0]
    assert card_heading.string == 'title'


def test_card_with_icon():
    card_content = {
        'title': 'title',
        'url': 'url',
        'description': 'description',
        'img_src': 'img_src',
        'img_alt': 'img_alt',
    }
    string = (
        "{{% load card_with_icon from directory_components_tags %}}"
        "{{% card_with_icon title='{title}' url='{url}' "
        "description='{description}' "
        "img_src='{img_src}' img_alt='{img_alt}' %}}"
        ).format(**card_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    card_link = soup.select('.card-link')[0]
    assert 'url' in card_link['href']

    card_image = soup.find('img')
    assert card_image['src'] == 'img_src'
    assert card_image['alt'] == 'img_alt'

    card_heading = soup.select('h3.heading-large')[0]
    assert card_heading.string == 'title'

    card_description = soup.select('p.description')[0]
    assert card_description.string == 'description'
