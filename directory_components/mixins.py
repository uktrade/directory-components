from directory_components.context_processors import (
    header_footer_processor,
    urls_processor
)
from django.conf import settings
from django.utils import translation

from directory_constants.choices import COUNTRY_CHOICES

from directory_components import helpers, forms


class CountryDisplayMixin:
    country_form_class = forms.CountryForm

    def get_context_data(self, *args, **kwargs):
        country_code = helpers.get_user_country(self.request)

        # if there is a country already detected we can hide the selector
        hide_country_selector = bool(country_code)
        country_name = dict(COUNTRY_CHOICES).get(country_code, '')

        country = {
            # used for flag icon css class. must be lowercase
            'code': country_code.lower(),
            'name': country_name,
        }

        country_form_kwargs = self.get_country_form_kwargs()

        return super().get_context_data(
            hide_country_selector=hide_country_selector,
            country=country,
            country_selector_form=self.country_form_class(
                **country_form_kwargs),
            *args, **kwargs
        )

    def get_country_form_kwargs(self, **kwargs):
        return {
            'initial': forms.get_country_form_initial_data(self.request),
            **kwargs,
        }


class EnableTranslationsMixin:
    template_name_bidi = None
    language_form_class = forms.LanguageForm

    def __init__(self, *args, **kwargs):
        dependency = 'directory_components.middleware.ForceDefaultLocale'
        if hasattr(settings, 'MIDDLEWARE_CLASSES'):
            assert dependency in settings.MIDDLEWARE_CLASSES
        else:
            assert dependency in settings.MIDDLEWARE
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        translation.activate(request.LANGUAGE_CODE)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['LANGUAGE_BIDI'] = translation.get_language_bidi()
        language_form_kwargs = self.get_language_form_kwargs()
        context['language_switcher'] = {
            'show': True,
            'form': self.language_form_class(**language_form_kwargs),
        }
        return context

    def get_language_form_kwargs(self, **kwargs):
        return {
            'initial': forms.get_language_form_initial_data(),
            **kwargs,
        }


class CMSLanguageSwitcherMixin:

    def dispatch(self, request, *args, **kwargs):
        translation.activate(request.LANGUAGE_CODE)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        form = forms.LanguageForm(
            initial={'lang': translation.get_language()},
            language_choices=self.page['meta']['languages']
        )
        show_language_switcher = (
            len(self.page['meta']['languages']) > 1 and
            form.is_language_available(translation.get_language())
        )
        return super().get_context_data(
            language_switcher={'form': form, 'show': show_language_switcher},
            *args,
            **kwargs
        )


class GA360Mixin:
    def __init__(self):
        self.ga360_payload = {}

    def set_ga360_payload(self, page_id, business_unit, site_section,
                          site_subsection=None):
        self.ga360_payload['page_id'] = page_id
        self.ga360_payload['business_unit'] = business_unit
        self.ga360_payload['site_section'] = site_section
        if site_subsection:
            self.ga360_payload['site_subsection'] = site_subsection

    def get_context_data(self, *args, **kwargs):
        self.ga360_payload['site_language'] = translation.get_language()

        try:
            self.ga360_payload['user_id'] = str(self.request.sso_user.id)
            self.ga360_payload['login_status'] = True
        except AttributeError:
            self.ga360_payload['user_id'] = None
            self.ga360_payload['login_status'] = False

        return super().get_context_data(
            ga360=self.ga360_payload,
            *args,
            **kwargs
        )


class InternationalHeaderMixin:
    def get_context_data(self, *args, **kwargs):

        header_footer_urls = header_footer_processor(None)['header_footer_urls']  # noqa
        services_urls = urls_processor(None)['services_urls']

        header_items = [
            {
                'name': 'about_uk',
                'title': 'About the UK',
                'url': 'https://great.uat.uktrade.io/international/the-uk/',  # noqa
                'sub_pages': [
                    {
                        'name': 'about_uk_home',
                        'title': 'Overview',
                        'url': 'https://great.uat.uktrade.io/international/the-uk/'  # noqa
                    },
                    {
                        'name': 'industries',
                        'title': 'Industries',
                        'url': header_footer_urls['industries']
                    },
                    {
                        'name': 'regions',
                        'title': 'Regions',
                        'url': 'https://great.uat.uktrade.io/international/the-uk/regions/'  # noqa
                    }
                ]
            },
            {
                'name': 'expand',
                'title': 'Start a company',
                'url': services_urls['invest'],
                'sub_pages': [
                    {
                        'name': 'expand_home',
                        'title': 'Overview',
                        'url': services_urls['invest']
                    },
                    {
                        'name': 'high_potential_opportunities',
                        'title': 'High-potential opportunities',
                        'url': services_urls['invest'] + '#high-potential-opportunities'  # noqa
                    },
                    {
                        'name': 'uk_setup_guide',
                        'title': 'How to set up a company',
                        'url': services_urls['uk_setup_guide']
                    },
                    {
                        'name': 'isd',
                        'title': 'Professional advice',
                        'url': services_urls['isd']
                    }
                ]
            },
            {
                'name': 'capital_invest',
                'title': 'Invest capital',
                'url': services_urls['capital_invest'],
                'sub_pages': [
                    {
                        'name': 'capital_invest_home',
                        'title': 'Overview',
                        'url': services_urls['capital_invest']
                    },
                    {
                        'name': 'investment_types',
                        'title': 'Investment types',
                        'url': 'https://great.uat.uktrade.io/international/invest-capital/types/'  # noqa
                    },
                    {
                        'name': 'investment_opportunities',
                        'title': 'Investment opportunities',
                        'url': 'https://great.uat.uktrade.io/international/invest-capital/opportunities/'  # noqa
                    },
                    {
                        'name': 'investment_guides',
                        'title': 'How to invest capital',
                        'url': 'https://great.uat.uktrade.io/international/invest-capital/guides/'  # noqa
                    },
                    {
                        'name': 'isd',
                        'title': 'Professional advice',
                        'url': services_urls['isd']
                    }
                ]
            },
            {
                'name': 'find_a_supplier',
                'title': 'Buy from the UK',
                'url': header_footer_urls['fas'],
                'sub_pages': [
                    {
                        'name': 'find_a_supplier_home',
                        'title': 'Overview',
                        'url': header_footer_urls['fas']
                    },
                    {
                        'name': 'import_guides',
                        'title': 'How to buy from the UK',
                        'url': 'https://great.uat.uktrade.io/international/import/guides/'  # noqa
                    },
                    {
                        'name': 'supplier_directory',
                        'title': 'Supplier directory',
                        'url': header_footer_urls['fas'] + '?q=&sectors='
                    }
                ]
            },
            {
                'name': 'about_dit',
                'title': 'About us',
                'url': 'https://great.uat.uktrade.io/international/about-dit/',
                'sub_pages': [
                    {
                        'name': 'about_dit_home',
                        'title': 'What we do',
                        'url': 'https://great.uat.uktrade.io/international/about-dit/'  # noqa
                    },
                    {
                        'name': 'dit_case_studies',
                        'title': 'Success stories',
                        'url': 'https://great.uat.uktrade.io/international/about-dit/case-studies/'  # noqa
                    },
                    {
                        'name': 'contact_us',
                        'title': 'Contact us',
                        'url': services_urls['contact_us']
                    }
                ]
            },
            {
                'name': 'news_and_events',
                'title': 'News and events',
                'url': 'https://great.uat.uktrade.io/international/latest/',
                'sub_pages': [
                    {
                        'name': 'news',
                        'title': 'News',
                        'url': 'https://www.gov.uk/government/organisations/department-for-international-trade'  # noqa
                    },
                    {
                        'name': 'events',
                        'title': 'Events',
                        'url': services_urls['events']
                    }
                ]
            }
        ]

        return super().get_context_data(
            international_header_area=self.international_header_area,
            international_header_selected_page=self.international_header_selected_page,  # noqa
            header_items=header_items,
            *args,
            **kwargs
        )
