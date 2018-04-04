import pytest

from django import forms

from directory_components import fields

REQUIRED_MESSAGE = fields.PaddedCharField.default_error_messages['required']


class PaddedTestForm(forms.Form):
    field = fields.PaddedCharField(fillchar='0', max_length=6)


def test_padded_field_padds_value():
    form = PaddedTestForm(data={'field': 'val'})

    assert form.is_valid()
    assert form.cleaned_data['field'] == '000val'


def test_padded_field_handles_empty():
    for value in ['', None]:
        form = PaddedTestForm(data={'field': value})

        assert form.is_valid() is False
        assert form.errors['field'] == [REQUIRED_MESSAGE]


@pytest.mark.parametrize('field_class', (
    fields.CharField,
    fields.URLField,
    fields.BooleanField,
))
def test_explicit_widget_attrs(field_class):
    field = field_class()

    field_explicit_attrs = field_class(
        widget=forms.TextInput(attrs={'class': 'a-class'})
    )

    assert field.widget.attrs['class'] == ' form-control'
    assert field_explicit_attrs.widget.attrs['class'] == 'a-class form-control'
