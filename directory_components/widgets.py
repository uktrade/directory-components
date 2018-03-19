from django.forms import widgets
from django import forms


class ChoiceWidget(widgets.ChoiceWidget):
    add_id_value = True

    def id_for_label(self, id_, value):
        """
        Patch to use the field value as an id suffix instead
        of using an incremented zero-based index.
        e.g. prefix-fieldname-value
        use hyphens not underscores
        """
        if id_ and self.add_id_value:
            id_ = '%s-%s' % (id_, value)
        return id_

    def create_option(
            self, name, value, label, selected, index,
            subindex=None, attrs=None):
        """
        Patch to use nicer ids.
        """
        index = str(index) if subindex is None else "%s-%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(
            self.attrs, attrs) if self.option_inherits_attrs else {}
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], value)
        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
            'wrap_label': True,
            }


class RadioSelect(ChoiceWidget):
    template_name = 'directory_components/multiple_input.html'
    option_template_name = 'directory_components/radio_option.html'
    css_class_name = 'select-multiple'
    input_type = 'radio'


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


class CheckboxSelectMultiple(ChoiceWidget):
    """
    Inherit from our patched ChoiceWidget and change nothing else.
    """
    pass


class CheckboxSelectInlineLabelMultiple(CheckboxSelectMultiple):
    template_name = 'directory_components/multiple_input.html'
    option_template_name = 'directory_components/checkbox_inline_multiple.html'
    css_class_name = 'select-multiple'
    input_type = 'checkbox'

    def __init__(self, attrs=None):
        super().__init__(attrs=attrs)
        self.attrs['class'] = self.attrs.get('class', self.css_class_name)
