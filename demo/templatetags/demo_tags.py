import inspect

from django import template

register = template.Library()


@register.filter
def view_instance_code(instance):
    return inspect.getsource(instance.__class__).strip()
