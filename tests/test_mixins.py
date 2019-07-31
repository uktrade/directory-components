import pytest

from unittest.mock import patch, Mock
from django.views.generic import TemplateView
from django.utils import translation

from directory_constants.choices import COUNTRY_CHOICES
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


def test_language_display_mixin(rf, settings):
    class TestView(mixins.EnableTranslationsMixin, TemplateView):
        template_name = 'core/base.html'

    # Test with usual settings first
    request = rf.get('/')
    request.LANGUAGE_CODE = ''
    response = TestView.as_view()(request)
    assert response.context_data['language_switcher']['form']

    # Test when MIDDLWARE_CLASSES setting is being used instead of MIDDLEWARE
    settings.MIDDLEWARE_CLASSES = settings.MIDDLEWARE
    settings.MIDDLEWARE = []

    request = rf.get('/')
    request.LANGUAGE_CODE = ''
    response = TestView.as_view()(request)
    assert response.context_data['language_switcher']['form']


def test_cms_language_switcher_one_language(rf):
    class MyView(mixins.CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'core/base.html'
        page = {
            'meta': {'languages': [('en-gb', 'English')]}
        }

    request = rf.get('/')
    request.LANGUAGE_CODE = ''
    with translation.override('de'):
        response = MyView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['language_switcher']['show'] is False


def test_cms_language_switcher_active_language_unavailable(rf):

    class MyView(mixins.CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'core/base.html'

        page = {
            'meta': {
                'languages': [('en-gb', 'English'), ('de', 'German')]
            }
        }

    request = rf.get('/')
    request.LANGUAGE_CODE = 'fr'

    response = MyView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['language_switcher']['show'] is False


def test_cms_language_switcher_active_language_available(rf):

    class MyView(mixins.CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'core/base.html'

        page = {
            'meta': {
                'languages': [('en-gb', 'English'), ('de', 'German')]
            }
        }

    request = rf.get('/')
    request.LANGUAGE_CODE = 'de'

    response = MyView.as_view()(request)

    assert response.status_code == 200
    context = response.context_data['language_switcher']
    assert context['show'] is True
    assert context['form'].initial['lang'] == 'de'


def test_ga360_mixin_for_logged_in_user(rf):
    class TestView(mixins.GA360Mixin, TemplateView):
        template_name = 'core/base.html'

        def __init__(self):
            super().__init__()
            self.set_ga360_payload(
                page_id='TestPageId',
                business_unit='Test App',
                site_section='Test Section',
                site_subsection='Test Page'
            )

    request = rf.get('/')
    request.sso_user = Mock(
        id=1234
    )

    with translation.override('de'):
        response = TestView.as_view()(request)

    assert response.context_data['ga360']
    ga360_data = response.context_data['ga360']
    assert ga360_data['page_id'] == 'TestPageId'
    assert ga360_data['business_unit'] == 'Test App'
    assert ga360_data['site_section'] == 'Test Section'
    assert ga360_data['site_subsection'] == 'Test Page'
    assert ga360_data['user_id'] == '1234'
    assert ga360_data['login_status'] is True
    assert ga360_data['site_language'] == 'de'


def test_ga360_mixin_for_anonymous_user(rf):
    class TestView(mixins.GA360Mixin, TemplateView):
        template_name = 'core/base.html'

        def __init__(self):
            super().__init__()
            self.set_ga360_payload(
                page_id='TestPageId',
                business_unit='Test App',
                site_section='Test Section',
                site_subsection='Test Page'
            )

    request = rf.get('/')
    # sso_user is not set.

    with translation.override('de'):
        response = TestView.as_view()(request)

    assert response.context_data['ga360']
    ga360_data = response.context_data['ga360']
    assert ga360_data['user_id'] is None
    assert ga360_data['login_status'] is False


def test_ga360_mixin_does_not_share_data_between_instances():
    class TestView(mixins.GA360Mixin):
        pass

    view_one = TestView()
    view_one.ga360_payload['Test Key'] = "Test Value"

    view_two = TestView()

    assert 'Test Key' not in view_two.ga360_payload


def test_international_header_mixin(rf):
    class TestView(mixins.InternationalHeaderMixin, TemplateView):
        header_section = 'invest'
        template_name = 'core/base.html'

    request = rf.get('/')
    response = TestView.as_view()(request)

    assert response.status_code == 200
    assert len(response.context_data['sub_header_items']) == 0
    assert len(response.context_data['pages']) == 4

    header_items = [(item[0], item[2]) for item in response.context_data['header_items']]  # NOQA
    assert header_items == [
        ('Invest', True),
        ('UK setup guide', False),
        ('Find a UK supplier', False),
        ('Industries', False),
    ]
