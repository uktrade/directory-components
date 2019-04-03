import pytest
from bs4 import BeautifulSoup

from django import forms
from django.template import Context, Template

from directory_components import fields
from directory_components.templatetags import directory_components_tags

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
    assert card_image['role'] == 'img'
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
    assert card_image['role'] == 'img'
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


def test_message_box_default():
    box_content = {
        'heading': 'heading',
        'description': 'description',
    }
    string = (
        "{{% load message_box from directory_components_tags %}}"
        "{{% message_box heading='{heading}' "
        "description='{description}' %}}"
        ).format(**box_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    box_heading = soup.select('h3.heading-medium')[0]
    assert box_heading.string == 'heading'

    box_description = soup.select('p.box-description')[0]
    assert box_description.string == 'description'


def test_message_box_custom():
    box_content = {
        'heading': 'heading',
        'heading_level': 'h4',
        'heading_class': 'great-red-text',
        'description': 'description',
        'box_class': 'border-great-red background-offwhite',
    }
    string = (
        "{{% load message_box from directory_components_tags %}}"
        "{{% message_box heading='{heading}' heading_level='{heading_level}' "
        "heading_class='{heading_class}' description='{description}' "
        "box_class='{box_class}' %}}"
        ).format(**box_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    box_heading = soup.select('h4.great-red-text')[0]
    assert box_heading.string == 'heading'

    box = soup.select('.message-box')[0]
    assert 'border-great-red' in box['class']
    assert 'background-offwhite' in box['class']

    box_description = soup.select('p.box-description')[0]
    assert box_description.string == 'description'


def test_cta_box_default():
    box_content = {
        'box_id': 'box_id',
        'heading': 'heading',
        'description': 'description',
        'button_text': 'button_text',
        'button_url': 'button_url',
    }
    string = (
        "{{% load cta_box from directory_components_tags %}}"
        "{{% cta_box box_id='{box_id}' heading='{heading}' "
        "description='{description}' "
        "button_text='{button_text}' button_url='{button_url}' %}}"
        ).format(**box_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    box_id = soup.find(id='box_id')
    assert box_id['id'] == 'box_id'

    box_heading = soup.select('h3.heading-medium')[0]
    assert box_heading.string == 'heading'

    box_description = soup.select('p.box-description')[0]
    assert box_description.string == 'description'

    box_button = soup.select('a.button')[0]
    assert box_button.string == 'button_text'
    assert box_button['href'] == 'button_url'


def test_cta_box_custom():
    box_content = {
        'box_id': 'box_id',
        'box_class': 'background-great-blue white-text',
        'heading': 'heading',
        'heading_level': 'h4',
        'heading_class': 'heading-small',
        'description': 'description',
        'button_text': 'button_text',
        'button_url': 'button_url',
    }
    string = (
        "{{% load cta_box from directory_components_tags %}}"
        "{{% cta_box box_id='{box_id}' heading='{heading}' "
        "box_class='{box_class}' heading_level='{heading_level}' "
        "heading_class='{heading_class}' description='{description}' "
        "button_text='{button_text}' button_url='{button_url}' %}}"
        ).format(**box_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    box = soup.select('.cta-box')[0]
    assert box['id'] == 'box_id'

    assert 'background-great-blue' in box['class']
    assert 'white-text' in box['class']

    box_heading = soup.select('h4.heading-small')[0]
    assert box_heading.string == 'heading'

    box_description = soup.select('p.box-description')[0]
    assert box_description.string == 'description'

    box_button = soup.select('a.button')[0]
    assert box_button.string == 'button_text'
    assert box_button['href'] == 'button_url'
    assert box_button['id'] == 'box_id-button'


def test_banner():
    banner_content = {
        'badge_content': 'Badge content',
        'banner_content': '<p>Banner content with a <a href="#">link</a></p>',
    }
    string = (
        "{{% load banner from directory_components_tags %}}"
        "{{% banner badge_content='{badge_content}' "
        "banner_content='{banner_content}' %}}"
        ).format(**banner_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    banner = soup.select('.information-banner')[0]
    assert banner['id'] == 'information-banner'

    badge = soup.select('.banner-badge span')[0]
    assert badge.string == 'Badge content'

    exp_banner_content = (
        '<div><p class="body-text">Banner content with a '
        '<a class="link" href="#">link</a></p></div>')

    banner_content = soup.select('.banner-content div:nth-of-type(2)')[0]
    assert str(banner_content) == exp_banner_content


def test_hero():
    hero_content = {
        'background_image_url': 'image.png',
        'hero_text': 'hero_text',
        'description': 'description',
    }
    string = (
        "{{% load hero from directory_components_tags %}}"
        "{{% hero background_image_url='{background_image_url}' "
        "hero_text='{hero_text}' description='{description}' %}}"
        ).format(**hero_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    banner = soup.find(id='hero-heading')
    assert 'hero_text' in banner.string
    assert 'heading-hero-generic-compact' in banner['class']

    assert 'hero-title-compact' in html

    banner = soup.find(id='hero-description')
    assert banner.string == 'description'


def test_hero_large_title():
    hero_content = {
        'background_image_url': 'image.png',
        'hero_text': 'hero_text',
        'description': 'description',
        'large_title': True,
    }
    string = (
        "{{% load hero from directory_components_tags %}}"
        "{{% hero background_image_url='{background_image_url}' "
        "hero_text='{hero_text}' description='{description}' "
        "large_title={large_title} %}}"
        ).format(**hero_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    banner = soup.find(id='hero-heading')
    assert 'hero_text' in banner.string
    assert 'heading-hero-generic' in banner['class']

    assert 'hero-title' in html

    banner = soup.find(id='hero-description')
    assert banner.string == 'description'


@pytest.mark.parametrize('template_tag', (
    directory_components_tags.cta_box,
    directory_components_tags.message_box,
    directory_components_tags.banner,
    directory_components_tags.hero,
    directory_components_tags.card,
    directory_components_tags.card_with_icon,
    directory_components_tags.labelled_card,
    directory_components_tags.labelled_image_card,
    directory_components_tags.image_with_caption,
    directory_components_tags.cta_card,
    directory_components_tags.cta_link,
    directory_components_tags.statistics_card_grid
))
def test_template_tag_kwargs(template_tag):
    test_kwargs = {
        'foo': 'foo',
        'bar': 'bar',
    }
    actual = template_tag(**test_kwargs)
    assert actual == test_kwargs


@pytest.mark.parametrize('heading', ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
def test_convert_headings_to(heading):
    actual = directory_components_tags.convert_headings_to(
        '<' + heading + '></' + heading + '>',
        'figure'
    )
    expected = '<figure></figure>'
    assert actual == expected


def test_convert_headings_to_does_not_convert_non_headings():
    actual = directory_components_tags.convert_headings_to(
        '<span></span>', 'figure'
    )
    expected = '<span></span>'
    assert actual == expected


def test_override_elements_css_class():
    actual = directory_components_tags.override_elements_css_class(
        '<h2 class="existing-class"></h2>',
        'h2,test-class'
    )
    expected = '<h2 class="test-class"></h2>'
    assert actual == expected


def test_override_elements_css_class_does_not_override_non_targets():
    actual = directory_components_tags.override_elements_css_class(
        '<h4 class="existing-class"></h4>',
        'h2,test-class'
    )
    expected = '<h4 class="existing-class"></h4>'
    assert actual == expected
