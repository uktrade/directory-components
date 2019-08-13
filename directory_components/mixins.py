from collections import namedtuple

from django.conf import settings
from django.utils import translation

from directory_constants.choices import COUNTRY_CHOICES

from directory_components import helpers, forms
from directory_components import international_header_links as page_links


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
        if getattr(settings, 'MIDDLEWARE', []):
            assert dependency in settings.MIDDLEWARE
        else:
            assert dependency in settings.MIDDLEWARE_CLASSES
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

HeaderNode = namedtuple('RootPage', 'page sub_pages')
HeaderItem = namedtuple('HeaderItem', 'title url is_active')


INTERNATIONAL_HEADER_PAGES_WIDE = [
    HeaderNode(
        page=page_links.EXPAND,
        sub_pages=[
            page_links.OVERVIEW_EXPAND,
            page_links.HOW_TO_EXPAND,
            page_links.ISD,
            page_links.CONTACT_EXPAND,
        ],
    ),
    HeaderNode(
        page=page_links.INVEST,
        sub_pages=[
            page_links.OVERVIEW_INVEST,
            page_links.INVESTMENT_TYPES,
            page_links.INVESTMENT_OPPORTUNITIES,
            page_links.HOW_TO_INVEST_CAPITAL,
            page_links.CONTACT_INVEST
        ],
    ),
    HeaderNode(
        page=page_links.FAS,
        sub_pages=[
            page_links.FAS,
            page_links.CONTACT_TRADE,
        ],
    ),
    HeaderNode(
        page=page_links.ABOUT_THE_UK,
        sub_pages=[
            page_links.OVERVIEW_ABOUT,
            page_links.WHY_THE_UK,
            page_links.INDUSTRIES,
            page_links.REGIONS,
            page_links.CONTACT_INTERNATIONAL_TRIAGE
        ],
    ),
    HeaderNode(
        page=page_links.ABOUT_DIT,
        sub_pages=[
            page_links.WHAT_WE_DO_EXPAND,
            page_links.WHAT_WE_DO_INVEST,
            page_links.WHAT_WE_DO_TRADE,
            page_links.CONTACT_INTERNATIONAL_TRIAGE,
        ],
    ),
]
INTERNATIONAL_HEADER_PAGES_NARROW_ABOUT_ON_LEFT = [
    HeaderNode(
        page=page_links.ABOUT_THE_UK,
        sub_pages=[
            page_links.WHY_THE_UK,
            page_links.INDUSTRIES,
            page_links.REGIONS,
            page_links.CONTACT_INTERNATIONAL_TRIAGE
        ]
    ),
    HeaderNode(
        page=page_links.EXPAND,
        sub_pages=[
            page_links.HOW_TO_EXPAND,
            page_links.ISD,
            page_links.WHAT_WE_DO_EXPAND,
            page_links.CONTACT_EXPAND
        ]
    ),
    HeaderNode(
        page=page_links.INVEST,
        sub_pages=[
            page_links.INVESTMENT_TYPES,
            page_links.INVESTMENT_OPPORTUNITIES,
            page_links.HOW_TO_INVEST_CAPITAL,
            page_links.WHAT_WE_DO_INVEST,
            page_links.CONTACT_INVEST
        ]
    ),
    HeaderNode(
        page=page_links.FAS,
        sub_pages=[
            page_links.HOW_TO_BUY,
            page_links.FAS,
            page_links.WHAT_WE_DO_TRADE,
            page_links.CONTACT_TRADE
        ]
    )
]
INTERNATIONAL_HEADER_PAGES_NARROW_ABOUT_ON_RIGHT = [
    HeaderNode(
        page=page_links.EXPAND,
        sub_pages=[
            page_links.HOW_TO_EXPAND,
            page_links.ISD,
            page_links.WHAT_WE_DO_EXPAND,
            page_links.CONTACT_EXPAND
        ]
    ),
    HeaderNode(
        page=page_links.INVEST,
        sub_pages=[
            page_links.INVESTMENT_TYPES,
            page_links.INVESTMENT_OPPORTUNITIES,
            page_links.HOW_TO_INVEST_CAPITAL,
            page_links.WHAT_WE_DO_INVEST,
            page_links.CONTACT_INVEST
        ]
    ),
    HeaderNode(
        page=page_links.FAS,
        sub_pages=[
            page_links.HOW_TO_BUY,
            page_links.FAS,
            page_links.WHAT_WE_DO_TRADE,
            page_links.CONTACT_TRADE
        ]
    ),
    HeaderNode(
        page=page_links.ABOUT_THE_UK,
        sub_pages=[
            page_links.WHY_THE_UK,
            page_links.INDUSTRIES,
            page_links.REGIONS,
            page_links.CONTACT_INTERNATIONAL_TRIAGE
        ]
    ),
]
INTERNATIONAL_HEADER_PAGES_NARROW_WITH_OVERVIEW = [
    HeaderNode(
        page=page_links.ABOUT_THE_UK,
        sub_pages=[
            page_links.OVERVIEW_ABOUT,
            page_links.WHY_THE_UK,
            page_links.INDUSTRIES,
            page_links.REGIONS,
            page_links.CONTACT_INTERNATIONAL_TRIAGE
        ]
    ),
    HeaderNode(
        page=page_links.EXPAND,
        sub_pages=[
            page_links.OVERVIEW_EXPAND,
            page_links.HOW_TO_EXPAND,
            page_links.ISD,
            page_links.WHAT_WE_DO_EXPAND,
            page_links.CONTACT_EXPAND
        ]
    ),
    HeaderNode(
        page=page_links.INVEST,
        sub_pages=[
            page_links.OVERVIEW_INVEST,
            page_links.INVESTMENT_TYPES,
            page_links.INVESTMENT_OPPORTUNITIES,
            page_links.HOW_TO_INVEST_CAPITAL,
            page_links.WHAT_WE_DO_INVEST,
            page_links.CONTACT_INVEST
        ]
    ),
    HeaderNode(
        page=page_links.FAS,
        sub_pages=[
            page_links.HOW_TO_BUY,
            page_links.FAS,
            page_links.WHAT_WE_DO_TRADE,
            page_links.CONTACT_TRADE
        ]
    )
]


class InternationalHeaderMixin:
    # header_section and header_subsection can be set in the views.
    header_section = ""
    header_subsection = ""

    @property
    def nodes(self):
        variant = self.request.GET.get('header-variant', '') or self.request.COOKIES.get('header-variant', '')

        if variant == 'wide':
            return INTERNATIONAL_HEADER_PAGES_WIDE
        if variant == 'narrow-about-on-right':
            return INTERNATIONAL_HEADER_PAGES_NARROW_ABOUT_ON_RIGHT
        if variant == 'narrow-with-overview-link':
            return INTERNATIONAL_HEADER_PAGES_NARROW_WITH_OVERVIEW
        else:
            return INTERNATIONAL_HEADER_PAGES_NARROW_ABOUT_ON_LEFT

    def get_active_page(self):
        return next(
            (node for node in self.nodes if node.page.name == self.header_section),
            None
        )

    def get_context_data(self, *args, **kwargs):
        header_items = [
            HeaderItem(
                title=node.page.title,
                url=node.page.url,
                is_active=node.page.name == self.header_section
            )
            for node in self.nodes
        ]

        active_page = self.get_active_page()
        sub_pages = active_page.sub_pages if active_page else []

        sub_header_items = [
            HeaderItem(title=page.title,
                       url=page.url,
                       is_active=page.name == self.header_subsection)
            for page in sub_pages
        ]

        return super().get_context_data(
            header_items=header_items,
            sub_header_items=sub_header_items,
            pages=self.nodes,
            *args,
            **kwargs
        )
