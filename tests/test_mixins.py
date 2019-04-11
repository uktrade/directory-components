import pytest

from unittest.mock import patch
from django.views.generic import TemplateView
from django.utils import translation

from directory_constants.constants.choices import COUNTRY_CHOICES
from directory_components import mixins


@pytest.mark.parametrize('country_code,country_name', COUNTRY_CHOICES)
@patch('directory_components.helpers.get_user_country')
def test_country_display_mixin(
    mock_country, country_code, country_name, rf
):
    class TestView(mixins.CountryDisplayMixin, TemplateView):
        template_name = 'core/base.html'

    mock_country.return_value = country_code

    request = rf.get('/')
    response = TestView.as_view()(request)

    assert response.context_data['hide_country_selector']
    assert response.context_data['country']['name'] == country_name
    assert response.context_data['country']['code'] == country_code.lower()


@patch('directory_components.helpers.get_user_country')
def test_country_display_mixin_no_country(mock_country, rf):
    class TestView(mixins.CountryDisplayMixin, TemplateView):
        template_name = 'core/base.html'

    mock_country.return_value = ''

    request = rf.get('/')
    response = TestView.as_view()(request)

    assert not response.context_data['hide_country_selector']
    assert not response.context_data['country']['name']
    assert not response.context_data['country']['code']


def test_language_display_mixin(rf):
    class TestView(mixins.EnableTranslationsMixin, TemplateView):
        template_name = 'core/base.html'

    request = rf.get('/')
    request.LANGUAGE_CODE = ''
    response = TestView.as_view()(request)

    assert response.context_data['language_switcher']['form']


def test_cms_language_switcher_one_language(rf):
    class MyView(mixins.CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'core/base.html'

        def get_context_data(self, *args, **kwargs):
            page = {
                'meta': {'languages': [('en-gb', 'English')]}
            }
            return super().get_context_data(page=page, *args, **kwargs)

    request = rf.get('/')
    with translation.override('de'):
        response = MyView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['language_switcher']['show'] is False


def test_cms_language_switcher_active_language_unavailable(rf):

    class MyView(mixins.CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'core/base.html'

        def get_context_data(self, *args, **kwargs):
            page = {
                'meta': {
                    'languages': [('en-gb', 'English'), ('de', 'German')]
                }
            }
            return super().get_context_data(page=page, *args, **kwargs)

    request = rf.get('/')
    with translation.override('fr'):
        response = MyView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['language_switcher']['show'] is False


def test_cms_language_switcher_active_language_available(rf):

    class MyView(mixins.CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'core/base.html'

        def get_context_data(self, *args, **kwargs):
            page = {
                'meta': {
                    'languages': [('en-gb', 'English'), ('de', 'German')]
                }
            }
            return super().get_context_data(page=page, *args, **kwargs)

    request = rf.get('/')
    with translation.override('de'):
        response = MyView.as_view()(request)

    assert response.status_code == 200
    context = response.context_data['language_switcher']
    assert context['show'] is True
    assert context['form'].initial['lang'] == 'de'
