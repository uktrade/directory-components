from django.utils import translation

from directory_components import forms


def test_get_language_form_initial_data():
    with translation.override('fr'):
        data = forms.get_language_form_initial_data()
        assert data['lang'] == 'fr'
