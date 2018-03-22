from django import forms
from directory_components.widgets import CheckboxSelectInlineLabelMultiple
from directory_components.widgets import CheckboxWithInlineLabel
from directory_components.widgets import RadioSelect


class DemoForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(DemoForm, self).__init__(auto_id='demo-%s', *args, **kwargs)

    DEMO_COLOURS = (
        ('red', 'Red'),
        ('green', 'Green'),
        ('blue', 'Blue'),
    )
    DEMO_CHOICES = (
        (True, 'Yes'),
        (False, 'No'),
    )
    DEMO_GROUPS = (
        ('Colours',
            (
                ('red', 'Red'),
                ('green', 'Green'),
                ('blue', 'Blue'),
            )),
        ('Numbers',
            (
                ('4', 'Four'),
                ('5', 'Five'),
                ('6', 'Six'),
            )),
    )
    checkbox1 = forms.BooleanField(
        required=False,
        label='',
        label_suffix='',
        widget=CheckboxWithInlineLabel(
            label='Label text',
            help_text='This is some help text. This help text is very long so '
            'you can see how it wraps next to the form elements. Very very '
            'long boring text that doesn\'t say anything. Why are you '
            'reading this?',
            attrs={'id': 'checkbox-one'}
        )
    )
    checkbox2 = forms.BooleanField(
        required=False,
        label='',
        label_suffix='',
        widget=CheckboxWithInlineLabel(
            label='Label text with no help text',
            attrs={'id': 'checkbox-two'}
        )
    )
    multiple_choice = forms.MultipleChoiceField(
        label='Multiple choice checkboxes',
        help_text='This is some help text.',
        label_suffix='',
        required=False,
        widget=CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-multiple'}
        ),
        choices=DEMO_COLOURS,
    )
    radio = forms.ChoiceField(
        label='Radio select',
        label_suffix='',
        help_text='Some help text.',
        widget=RadioSelect(
            use_nice_ids=True,
            attrs={'id': 'radio-one'}),
        choices=DEMO_CHOICES
    )
    radio_group = forms.ChoiceField(
        label='Radio select with option groups',
        label_suffix='',
        help_text='Some help text.',
        widget=RadioSelect(
            use_nice_ids=True,
            attrs={'id': 'radio-two'}),
        choices=DEMO_GROUPS
    )
