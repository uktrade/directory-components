import pytest

from unittest.mock import patch
from django.views.generic import TemplateView

from directory_constants.constants.choices import COUNTRY_CHOICES
from directory_components.mixins import (
    CountryDisplayMixin, LanguageSwitcherMixin
)


@pytest.mark.parametrize('country_code,country_name', COUNTRY_CHOICES)
@patch('directory_components.helpers.get_user_country')
def test_country_display_mixin(
    mock_country, country_code, country_name, rf
):
    class TestView(CountryDisplayMixin, TemplateView):
        template_name = 'core/base.html'

    mock_country.return_value = country_code

    request = rf.get('/')
    response = TestView.as_view()(request)

    assert response.context_data['hide_country_selector']
    assert response.context_data['country']['name'] == country_name
    assert response.context_data['country']['code'] == country_code.lower()


@patch('directory_components.helpers.get_user_country')
def test_country_display_mixin_no_country(mock_country, rf):
    class TestView(CountryDisplayMixin, TemplateView):
        template_name = 'core/base.html'

    mock_country.return_value = ''

    request = rf.get('/')
    response = TestView.as_view()(request)

    assert not response.context_data['hide_country_selector']
    assert not response.context_data['country']['name']
    assert not response.context_data['country']['code']


def test_language_display_mixin(rf):
    class TestView(LanguageSwitcherMixin, TemplateView):
        template_name = 'core/base.html'

    request = rf.get('/')
    response = TestView.as_view()(request)

    assert response.context_data['language_switcher_form']
