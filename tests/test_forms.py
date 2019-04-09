from django.utils import translation

from directory_components.forms import get_language_form_initial_data


def test_get_language_form_initial_data():
    translation.activate('fr')
    request_stub = {}
    data = get_language_form_initial_data(request_stub)
    assert data['lang'] == 'fr'
