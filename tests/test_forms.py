from bs4 import BeautifulSoup

from django.utils import translation

from directory_components import forms


def test_get_language_form_initial_data():
    with translation.override('fr'):
        data = forms.get_language_form_initial_data()
        assert data['lang'] == 'fr'


def test_form_render():
    class Form(forms.Form):
        field = forms.CharField()

    form = Form()

    expected = """
        <div class=" form-group" id="id_field-container">
            <label class=" form-label" for="id_field">Field</label>
            <input type="text" name="field" class=" form-control" id="id_field">
        </div>
    """

    actual = str(form)

    assert BeautifulSoup(actual, 'html.parser') == BeautifulSoup(expected, 'html.parser')
