import pytest

from django.forms import TextInput

from directory_components import forms


REQUIRED_MESSAGE = forms.PaddedCharField.default_error_messages['required']


class PaddedTestForm(forms.Form):
    field = forms.PaddedCharField(fillchar='0', max_length=6)


def test_padded_field_padds_value():
    form = PaddedTestForm(data={'field': 'val'})

    assert form.is_valid()
    assert form.cleaned_data['field'] == '000val'


def test_padded_field_handles_empty():
    for value in ['', None]:
        form = PaddedTestForm(data={'field': value})

        assert form.is_valid() is False
        assert form.errors['field'] == [REQUIRED_MESSAGE]


field_classes = (
    forms.BooleanField,
    forms.CharField,
    forms.ChoiceField,
    forms.DateField,
    forms.EmailField,
    forms.IntegerField,
    forms.MultipleChoiceField,
    forms.URLField,
)


@pytest.mark.parametrize('field_class', field_classes)
def test_explicit_widget_attrs(field_class):
    field = field_class()

    field_explicit_attrs = field_class(
        widget=TextInput(attrs={'class': 'a-class'})
    )

    assert field.widget.attrs['class'] == ' form-control'
    assert field_explicit_attrs.widget.attrs['class'] == 'a-class form-control'


@pytest.mark.parametrize('field_class', field_classes)
def test_container_class(field_class):
    class MyForm(forms.Form):
        field = field_class(container_css_classes='border-purple')

    form = MyForm()

    assert form['field'].css_classes() == ' border-purple'
