from django import forms
from django.forms.boundfield import BoundField

from directory_components.forms import widgets


__all__ = [
    'BooleanField',
    'CharField',
    'ChoiceField',
    'DateField',
    'DirectoryComponentsBoundField',
    'DirectoryComponentsFieldMixin',
    'EmailField',
    'field_factory',
    'IntegerField',
    'MultipleChoiceField',
    'PaddedCharField',
    'URLField',
]


class DirectoryComponentsBoundField(BoundField):
    def label_tag(self, contents=None, attrs=None, label_suffix=None):
        attrs = attrs or {}
        attrs['class'] = attrs.get('class', '') + ' form-label'
        return super().label_tag(
            contents=contents,
            attrs=attrs,
            label_suffix=label_suffix
        )

    def css_classes(self, *args, **kwargs):
        css_classes = super().css_classes(*args, **kwargs)
        return f'{css_classes} {self.field.container_css_classes}'


class DirectoryComponentsFieldMixin:

    def __init__(self, container_css_classes='form-group', *args, **kwargs):
        self.container_css_classes = container_css_classes
        super().__init__(*args, **kwargs)
        if not hasattr(self.widget, 'css_class_name'):
            self.widget.attrs['class'] = (
                self.widget.attrs.get('class', '') + ' form-control'
            )
        self.label_suffix = ''

    def get_bound_field(self, form, field_name):
        return DirectoryComponentsBoundField(form, self, field_name)


def field_factory(base_class):
    bases = (DirectoryComponentsFieldMixin, base_class)
    return type(base_class.__name__, bases, {})


CharField = field_factory(forms.CharField)
EmailField = field_factory(forms.EmailField)
URLField = field_factory(forms.URLField)
ChoiceField = field_factory(forms.ChoiceField)
DateField = field_factory(forms.DateField)
IntegerField = field_factory(forms.IntegerField)
MultipleChoiceField = field_factory(forms.MultipleChoiceField)


class BooleanField(DirectoryComponentsFieldMixin, forms.BooleanField):
    def __init__(self, label='', help_text='', widget=None, *args, **kwargs):
        if widget is None:
            widget = widgets.CheckboxWithInlineLabel()
        if isinstance(widget, widgets.CheckboxWithInlineLabel):
            widget.label = label
            widget.help_text = help_text
            label = ''
        super().__init__(label=label, widget=widget, *args, **kwargs)


class PaddedCharField(CharField):
    def __init__(self, fillchar, *args, **kwargs):
        self.fillchar = fillchar
        super().__init__(*args, **kwargs)

    def to_python(self, *args, **kwargs):
        value = super().to_python(*args, **kwargs)
        if value not in self.empty_values:
            return value.rjust(self.max_length, self.fillchar)
        return value
