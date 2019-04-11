from django.utils import translation

from directory_components import forms


def test_get_language_form_initial_data():
    translation.activate('fr')
    request_stub = {}
    data = forms.get_language_form_initial_data(request_stub)
    assert data['language'] == 'fr'


def test_get_lang_form_initial_data():
    translation.activate('fr')
    request_stub = {}
    data = forms.get_lang_form_initial_data(request_stub)
    assert data['lang'] == 'fr'
