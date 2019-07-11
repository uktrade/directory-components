from directory_components import forms


class PrefixIdMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(auto_id='demo-%s', *args, **kwargs)


class TextBoxForm(PrefixIdMixin, forms.Form):
    text_field1 = forms.CharField(
        label='Q1: Simple text field',
        help_text='Some help text'
    )
    url_field = forms.URLField(
        label='Q2: URL field',
        help_text='Some help text'
    )
    email_field = forms.EmailField(
        label='Q3: Email field',
        help_text='Some email field help text',
    )
    choice_field = forms.ChoiceField(
        label='Q4: select field',
        help_text='Some help text',
        choices=[
            ('red', 'Red'),
            ('green', 'Green'),
            ('blue', 'Blue'),
        ]
    )
    text_field2 = forms.CharField(
        label='Q5: Custom css class on container',
        help_text='Some help text',
        container_css_classes='border-purple border-thin padding-30',
    )


class CheckboxForm(PrefixIdMixin, forms.Form):
    checkbox1 = forms.BooleanField(
        label='Q1: Label text',
        help_text=(
            'This is some help text. This help text is very long so '
            'you can see how it wraps next to the form elements. Very very '
            'long boring text that doesn\'t say anything. Why are you '
            'reading this?'
        ),
        widget=forms.CheckboxWithInlineLabel(
            attrs={'id': 'checkbox-one'}
        )
    )
    checkbox2 = forms.BooleanField(
        label='Q2: Label text with no help text',
        widget=forms.CheckboxWithInlineLabel(
            attrs={'id': 'checkbox-two'}
        )
    )


class MultipleChoiceForm(PrefixIdMixin, forms.Form):
    multiple_choice = forms.MultipleChoiceField(
        label='Q1: Multiple choice checkboxes',
        help_text='This is some help text.',
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-multiple'},
            use_nice_ids=True,
        ),
        choices=(
            ('red', 'Red'),
            ('green', 'Green'),
            ('blue', 'Blue'),
        ),
    )


class RadioForm(PrefixIdMixin, forms.Form):
    radio = forms.ChoiceField(
        label='Q1: Radio select',
        label_suffix='',
        help_text='Some help text.',
        widget=forms.RadioSelect(
            use_nice_ids=True,
            attrs={'id': 'radio-one'}
        ),
        choices=(
            (True, 'Yes'),
            (False, 'No'),
        )
    )
    radio_group = forms.ChoiceField(
        label='Q2: Radio select with option groups',
        label_suffix='',
        help_text='Some help text.',
        widget=forms.RadioSelect(
            use_nice_ids=True,
            attrs={'id': 'radio-two'}
        ),
        choices=(
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
    )


class DemoFormErrors(PrefixIdMixin, forms.Form):

    text_field1 = forms.CharField(
        label='Simple text field',
        help_text='Some help text',
        required=True
    )
    checkbox1 = forms.BooleanField(
        label='Label text',
        required=True,
        help_text=(
            'Some help text.'
        ),
        widget=forms.CheckboxWithInlineLabel(
            attrs={'id': 'checkbox-one'}
        )
    )
    multiple_choice = forms.MultipleChoiceField(
        label='Multiple choice checkboxes',
        required=True,
        help_text='Some help text.',
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-multiple'},
            use_nice_ids=True,
        ),
        choices=(
            ('red', 'Red'),
            ('green', 'Green'),
            ('blue', 'Blue'),
        ),
    )

    radio = forms.ChoiceField(
        label='Radio select',
        required=True,
        label_suffix='',
        help_text='Some help text.',
        widget=forms.RadioSelect(
            use_nice_ids=True,
            attrs={'id': 'radio-one'}
        ),
        choices=(
            (True, 'Yes'),
            (False, 'No'),
        )
    )
