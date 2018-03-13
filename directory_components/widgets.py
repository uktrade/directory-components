from django.utils.safestring import mark_safe
from django.forms import widgets
from django import forms


class RadioSelect(widgets.RadioSelect):
    template_name = 'directory_components/radio.html'
    option_template_name = 'directory_components/radio_option.html'


class CheckboxWithInlineLabel(forms.widgets.CheckboxInput):
    template_name = 'directory_components/checkbox_inline.html'

    def __init__(self, label='', help_text=None, *args, **kwargs):
        self.label = label
        self.help_text = help_text
        super().__init__(*args, **kwargs)

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context['label'] = self.label
        context['help_text'] = self.help_text
        return context


class ComponentsCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'directory_components/checkbox_select.html'


class CheckboxSelectInlineLabelMultiple(ComponentsCheckboxSelectMultiple):
    option_template_name = 'directory_components/checkbox_inline_multiple.html'
    css_class_name = 'checkbox-multiple'

    def __init__(self, attrs=None):
        super().__init__(attrs=attrs)
        self.attrs['class'] = self.attrs.get('class', self.css_class_name)
