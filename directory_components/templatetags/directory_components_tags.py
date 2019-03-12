from bs4 import BeautifulSoup
import re

from django import template
from django.templatetags import static
from django.utils.text import slugify, mark_safe, wrap

register = template.Library()


class FullStaticNode(static.StaticNode):
    def url(self, context):
        request = context['request']
        return request.build_absolute_uri(super().url(context))


@register.tag
def static_absolute(parser, token):
    return FullStaticNode.handle_token(parser, token)


@register.filter
def split_lines(text, length):
    lines = wrap(text, length).split('\n')
    output = ''.join(['<span>' + line + '</span><br>' for line in lines])
    return mark_safe(output)


def build_anchor_id(element, suffix):
    return slugify(get_label(element) + suffix)


def get_label(element):
    return re.sub(r'^.* \- ', '', element.contents[0])


@register.filter
def add_anchors(value, suffix=''):
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll('h2'):
        element.attrs['id'] = build_anchor_id(element, suffix)
    return mark_safe(str(soup))


@register.filter
def add_export_elements_classes(value):
    soup = BeautifulSoup(value, 'html.parser')
    mapping = [
        ('h1', 'heading-xlarge'),
        ('h2', 'heading-large'),
        ('h3', 'heading-medium'),
        ('h4', 'heading-small'),
        ('h5', 'heading-small'),
        ('h6', 'heading-small'),
        ('ul', 'list list-bullet'),
        ('ol', 'list list-number'),
        ('p', 'body-text'),
        ('a', 'link'),
        ('blockquote', 'quote'),
    ]
    for tag_name, class_name in mapping:
        for element in soup.findAll(tag_name):
            element.attrs['class'] = class_name
    return mark_safe(str(soup))


@register.filter
def convert_headings_to(value, heading):
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        element.name = heading
    return str(soup)


@register.filter
def override_elements_css_class(value, element_and_override):
    arguments = element_and_override.split(',')
    element_type = arguments[0]
    override = arguments[1]
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll(element_type):
        element.attrs['class'] = override
    return str(soup)


@register.inclusion_tag('directory_components/form_widgets/form.html')
def render_form(form):
    return {'form': form}


@register.inclusion_tag('directory_components/cta_box.html')
def cta_box(**kwargs):
    return kwargs


@register.inclusion_tag('directory_components/message_box.html')
def message_box(**kwargs):
    return kwargs


@register.inclusion_tag('directory_components/banner.html')
def banner(**kwargs):
    return kwargs


@register.inclusion_tag('directory_components/hero.html')
def hero(**kwargs):
    return kwargs


@register.inclusion_tag('directory_components/card.html')
def card(**kwargs):
    return kwargs


@register.inclusion_tag('directory_components/card_with_icon.html')
def card_with_icon(**kwargs):
    return kwargs


@register.inclusion_tag('directory_components/labelled_card.html')
def labelled_card(**kwargs):
    return kwargs


@register.inclusion_tag('directory_components/labelled_image_card.html')
def labelled_image_card(**kwargs):
    return kwargs


@register.inclusion_tag('directory_components/image_with_caption.html')
def image_with_caption(**kwargs):
    return kwargs


@register.inclusion_tag('directory_components/cta_card.html')
def cta_card(**kwargs):
    return kwargs


@register.inclusion_tag('directory_components/cta_link.html')
def cta_link(**kwargs):
    return kwargs
