from django import forms
from directory_components.widgets import CheckboxSelectInlineLabelMultiple
from directory_components.widgets import CheckboxWithInlineLabel


class DemoForm(forms.Form):
    COLOURS_CHOICES = (
        ('1', 'One'),
        ('2', 'Two'),
        ('3', 'Three'),
    )
    checkbox1 = forms.BooleanField(
        required=False,
        label='',
        label_suffix='',
        widget=CheckboxWithInlineLabel(
            label='Label text',
            help_text='This is some hint text. This hint text is very long so '
            'you can see how it wraps next to the form elements. Very very '
            'long boring text that doesn\'t say anything. Why are you '
            'reading this?',
            attrs={'id': 'checkbox1'}
        )
    )
    checkbox2 = forms.BooleanField(
        required=False,
        label='',
        label_suffix='',
        widget=CheckboxWithInlineLabel(
            label='Label text with no hint text',
        )
    )
    multiple_choice = forms.MultipleChoiceField(
        label='Multiple choice field',
        help_text='This is some hint text.',
        label_suffix='',
        required=False,
        widget=CheckboxSelectInlineLabelMultiple(),
        choices=COLOURS_CHOICES,
    )
