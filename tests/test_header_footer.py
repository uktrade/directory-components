from bs4 import BeautifulSoup
from directory_constants.constants import urls
import pytest

from django.template.loader import render_to_string

from directory_components import context_processors


@pytest.mark.parametrize('template_name', [
    'directory_components/header_footer_old/header.html',
    'directory_components/header_footer_old/footer.html',
    'directory_components/header_footer_old/header_static.html',
    'directory_components/header_footer/international_header.html',
    'directory_components/header_footer/international_footer.html',
    'directory_components/header_footer/domestic_header.html',
    'directory_components/header_footer/domestic_footer.html',
    'directory_components/header_footer/domestic_header_static.html',
])
def test_templates_rendered(template_name):
    html = render_to_string(template_name)
    assert '<div' in html
    assert '<ul' in html
    assert '<a' in html


@pytest.mark.parametrize('template_name', (
    'directory_components/header_footer_old/header.html',
    'directory_components/header_footer/domestic_header.html',
    )
)
def test_header_logged_in(template_name):
    context = {
        'sso_is_logged_in': True,
        'sso_login_url': 'login.com',
        'sso_logout_url': 'logout.com',
        **context_processors.header_footer_processor(None),
    }
    html = render_to_string(template_name, context)
    assert 'Sign in' not in html
    assert context['sso_login_url'] not in html
    assert 'Sign out' in html
    assert context['sso_logout_url'] in html


@pytest.mark.parametrize('template_name', (
    'directory_components/header_footer_old/header.html',
    'directory_components/header_footer/domestic_header.html',
    )
)
def test_header_logged_out(template_name):
    context = {
        'sso_is_logged_in': False,
        'sso_login_url': 'login.com',
        'sso_logout_url': 'logout.com',
        **context_processors.header_footer_processor(None),
    }
    html = render_to_string(template_name, context)
    assert 'Sign in' in html
    assert context['sso_login_url'] in html
    assert 'Sign out' not in html
    assert context['sso_logout_url'] not in html


@pytest.mark.parametrize('url', [
    urls.SERVICES_GREAT_DOMESTIC,
    urls.ADVICE_CREATE_AN_EXPORT_PLAN,
    urls.ADVICE_FIND_AN_EXPORT_MARKET,
    urls.ADVICE_DEFINE_ROUTE_TO_MARKET,
    urls.ADVICE_GET_EXPORT_FINANCE_AND_FUNDING,
    urls.ADVICE_MANAGE_PAYMENT_FOR_EXPORT_ORDERS,
    urls.ADVICE_PREPARE_TO_DO_BUSINESS_IN_A_FOREIGN_COUNTRY,
    urls.ADVICE_MANAGE_LEGAL_AND_ETHICAL_COMPLIANCE,
    urls.ADVICE_PREPARE_FOR_EXPORT_PROCEDURES_AND_LOGISTICS,
    urls.SERVICES_EXOPPS,
    urls.GET_FINANCE,
])
def test_urls_exist_in_header(url, settings):
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None)
    }
    template_name = 'directory_components/header_footer_old/header.html'
    assert url in render_to_string(template_name, context)


def test_header_v2_domestic_news_section_off(settings):
    context = {
        'features': {'NEWS_SECTION_ON': False},
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None)
    }
    template_name = 'directory_components/header_footer/domestic_header.html'
    html = render_to_string(template_name, context)
    assert urls.GREAT_DOMESTIC_NEWS not in html


def test_header_v2_international_news_section_off(settings):
    context = {
        'features': {'NEWS_SECTION_ON': False},
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None)
    }
    template_name = 'directory_components/header_footer/domestic_header.html'
    html = render_to_string(template_name, context)
    assert urls.GREAT_INTERNATIONAL_NEWS not in html


@pytest.mark.parametrize('url', [
    urls.SERVICES_GREAT_DOMESTIC,
    urls.GREAT_INTERNATIONAL,
    urls.ADVICE,
    urls.MARKETS,
    urls.SERVICES_FAB,
    urls.SERVICES_SOO,
    urls.SERVICES_EXOPPS,
    urls.GET_FINANCE,
    urls.SERVICES_EVENTS,
    urls.GREAT_DOMESTIC_NEWS,
])
def test_urls_exist_in_domestic_header_v2(url, settings):
    context = {
        'features': {'NEWS_SECTION_ON': True},
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None)
    }
    template_name = (
        'directory_components/header_footer/domestic_header.html')
    assert url in render_to_string(template_name, context)


@pytest.mark.parametrize('url', [
    urls.SERVICES_GREAT_DOMESTIC,
    urls.GREAT_INTERNATIONAL,
    urls.SERVICES_INVEST,
    urls.FAS_SEARCH,
    urls.GREAT_INTERNATIONAL_INDUSTRIES,
    urls.GREAT_INTERNATIONAL_HOW_TO_DO_BUSINESS_WITH_THE_UK,
    urls.GREAT_INTERNATIONAL_NEWS,
])
def test_urls_exist_in_international_header_v2(url, settings):
    context = {
        'features': {'NEWS_SECTION_ON': True},
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None)
    }
    template_name = (
        'directory_components/header_footer/international_header.html')
    assert url in render_to_string(template_name, context)


@pytest.mark.parametrize('url', [
    urls.SERVICES_GREAT_DOMESTIC,
    urls.ADVICE_CREATE_AN_EXPORT_PLAN,
    urls.ADVICE_FIND_AN_EXPORT_MARKET,
    urls.ADVICE_DEFINE_ROUTE_TO_MARKET,
    urls.ADVICE_GET_EXPORT_FINANCE_AND_FUNDING,
    urls.ADVICE_MANAGE_PAYMENT_FOR_EXPORT_ORDERS,
    urls.ADVICE_PREPARE_TO_DO_BUSINESS_IN_A_FOREIGN_COUNTRY,
    urls.ADVICE_MANAGE_LEGAL_AND_ETHICAL_COMPLIANCE,
    urls.ADVICE_PREPARE_FOR_EXPORT_PROCEDURES_AND_LOGISTICS,
    urls.SERVICES_EXOPPS,
    urls.GET_FINANCE,
    urls.ABOUT,
    urls.PRIVACY_AND_COOKIES,
    urls.TERMS_AND_CONDITIONS,
    urls.SERVICES_FAB,
    urls.SERVICES_SOO,
    urls.SERVICES_EVENTS,
    urls.CONTACT_US,
    urls.DIT,
])
def test_urls_exist_in_footer(url, settings):
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    template_name = 'directory_components/header_footer_old/footer.html'
    assert url in render_to_string(template_name, context)


@pytest.mark.parametrize('url', [
    urls.GREAT_INTERNATIONAL,
    urls.CONTACT_US,
    urls.PRIVACY_AND_COOKIES,
    urls.TERMS_AND_CONDITIONS,
    urls.DIT,
])
def test_urls_exist_in_domestic_footer_v2(url, settings):
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    template_name = (
        'directory_components/header_footer/domestic_footer.html')
    assert url in render_to_string(template_name, context)


@pytest.mark.parametrize('url', [
    urls.SERVICES_GREAT_DOMESTIC,
    urls.CONTACT_US,
    urls.PRIVACY_AND_COOKIES,
    urls.TERMS_AND_CONDITIONS,
    urls.DIT,
])
def test_urls_exist_in_international_footer_v2(url, settings):
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    template_name = (
        'directory_components/header_footer/international_footer.html')
    assert url in render_to_string(template_name, context)


@pytest.mark.parametrize('title,element_id,url', (
    (
        'Create an export plan',
        'header-advice-create-an-export-plan',
        urls.ADVICE_CREATE_AN_EXPORT_PLAN,
    ),
    (
        'Find an export market',
        'header-advice-find-an-export-market',
        urls.ADVICE_FIND_AN_EXPORT_MARKET,
    ),
    (
        'Define route to market',
        'header-advice-define-route-to-market',
        urls.ADVICE_DEFINE_ROUTE_TO_MARKET,
    ),
    (
        'Get export finance and funding',
        'header-advice-get-export-finance-and-funding',
        urls.ADVICE_GET_EXPORT_FINANCE_AND_FUNDING,
    ),
    (
        'Manage payment for export orders',
        'header-advice-manage-payment-for-export-orders',
        urls.ADVICE_MANAGE_PAYMENT_FOR_EXPORT_ORDERS,
    ),
    (
        'Prepare to do business in a foreign country',
        'header-advice-prepare-to-do-business-in-a-foreign-country',
        urls.ADVICE_PREPARE_TO_DO_BUSINESS_IN_A_FOREIGN_COUNTRY,
    ),
    (
        'Manage legal and ethical compliance',
        'header-advice-manage-legal-and-ethical-compliance',
        urls.ADVICE_MANAGE_LEGAL_AND_ETHICAL_COMPLIANCE,
    ),
    (
        'Prepare for export procedures and logistics',
        'header-advice-prepare-for-export-procedures-and-logistics',
        urls.ADVICE_PREPARE_FOR_EXPORT_PROCEDURES_AND_LOGISTICS,
    ),
    (
        None,
        'header-services-find-a-buyer',
        urls.SERVICES_FAB,
    ),
    (
        None,
        'header-services-selling-online-overseas',
        urls.SERVICES_SOO,
    ),
    (
        None,
        'header-services-export-opportunities',
        urls.SERVICES_EXOPPS,
    ),
    (
        None,
        'header-services-get-finance',
        urls.GET_FINANCE,
    ),
    (
        None,
        'header-services-events',
        urls.SERVICES_EVENTS,
    )
))
def test_header_ids_match_urls_and_text(
    title, element_id, url, settings
):
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }

    html = render_to_string(
        'directory_components/header_footer_old/header.html', context
    )
    soup = BeautifulSoup(html, 'html.parser')

    element = soup.find(id=element_id)

    assert element.attrs['href'] == url
    if title:
        assert element.string == title


@pytest.mark.parametrize('title,element_id,url', (
    (
        'Advice',
        'header-advice',
        urls.ADVICE,
    ),
    (
        'Markets',
        'header-markets',
        urls.MARKETS,
    ),
    (
        'Create a business profile',
        'header-services-business-profile',
        urls.SERVICES_FAB,
    ),
    (
        'Sell online overseas',
        'header-services-selling-online-overseas',
        urls.SERVICES_SOO,
    ),
    (
        'Find export opportunities',
        'header-services-export-opportunities',
        urls.SERVICES_EXOPPS,
    ),
    (
        'Get finance',
        'header-services-get-finance',
        urls.GET_FINANCE,
    ),
    (
        'Find events and visits',
        'header-services-events',
        urls.SERVICES_EVENTS,
    ),
    (
        'Get an EORI number',
        'header-services-eori',
        'https://www.gov.uk/eori',
    ),
    (
        'News and events',
        'header-news',
        urls.GREAT_DOMESTIC_NEWS,
    ),
))
def test_domestic_header_v2_ids_match_urls_and_text(
    title, element_id, url, settings
):
    context = {
        'features': {
            'NEWS_SECTION_ON': True,
            'NEW_HEADER_FOOTER_ON': True,
        },
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
    }

    html = render_to_string(
        'directory_components/header_footer/domestic_header.html', context
    )
    soup = BeautifulSoup(html, 'html.parser')

    element = soup.find(id=element_id)

    assert element.attrs['href'] == url
    if title:
        assert element.string == title


@pytest.mark.parametrize('title,element_id,url', (
    (
        'Invest',
        'header-invest',
        urls.SERVICES_INVEST,
    ),
    (
        'Find a UK supplier',
        'header-fas-search',
        urls.FAS_SEARCH,
    ),
    (
        'Industries',
        'header-industries',
        urls.GREAT_INTERNATIONAL_INDUSTRIES,
    ),
    (
        'How to do business with the UK',
        'header-how-to-do-business-with-the-uk',
        urls.GREAT_INTERNATIONAL_HOW_TO_DO_BUSINESS_WITH_THE_UK,
    ),
    (
        'News',
        'header-news',
        urls.GREAT_INTERNATIONAL_NEWS,
    ),
))
def test_international_header_v2_ids_match_urls_and_text(
    title, element_id, url, settings
):
    context = {
        'features': {
            'NEWS_SECTION_ON': True,
            'NEW_HEADER_FOOTER_ON': True,
        },
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
    }

    html = render_to_string(
        'directory_components/header_footer/international_header.html',
        context
    )
    soup = BeautifulSoup(html, 'html.parser')

    element = soup.find(id=element_id)

    assert element.attrs['href'] == url
    if title:
        assert element.string == title


@pytest.mark.parametrize('title,element_id,url', (
    (
        'Create an export plan',
        'footer-advice-create-an-export-plan',
        urls.ADVICE_CREATE_AN_EXPORT_PLAN,
    ),
    (
        'Find an export market',
        'footer-advice-find-an-export-market',
        urls.ADVICE_FIND_AN_EXPORT_MARKET,
    ),
    (
        'Define route to market',
        'footer-advice-define-route-to-market',
        urls.ADVICE_DEFINE_ROUTE_TO_MARKET,
    ),
    (
        'Get export finance and funding',
        'footer-advice-get-export-finance-and-funding',
        urls.ADVICE_GET_EXPORT_FINANCE_AND_FUNDING,
    ),
    (
        'Manage payment for export orders',
        'footer-advice-manage-payment-for-export-orders',
        urls.ADVICE_MANAGE_PAYMENT_FOR_EXPORT_ORDERS,
    ),
    (
        'Prepare to do business in a foreign country',
        'footer-advice-prepare-to-do-business-in-a-foreign-country',
        urls.ADVICE_PREPARE_TO_DO_BUSINESS_IN_A_FOREIGN_COUNTRY,
    ),
    (
        'Manage legal and ethical compliance',
        'footer-advice-manage-legal-and-ethical-compliance',
        urls.ADVICE_MANAGE_LEGAL_AND_ETHICAL_COMPLIANCE,
    ),
    (
        'Prepare for export procedures and logistics',
        'footer-advice-prepare-for-export-procedures-and-logistics',
        urls.ADVICE_PREPARE_FOR_EXPORT_PROCEDURES_AND_LOGISTICS,
    ),
    (
        None,
        'footer-services-find-a-buyer',
        urls.SERVICES_FAB,
    ),
    (
        None,
        'footer-services-selling-online-overseas',
        urls.SERVICES_SOO,
    ),
    (
        None,
        'footer-services-export-opportunities',
        urls.SERVICES_EXOPPS,
    ),
    (
        None,
        'footer-services-get-finance',
        urls.GET_FINANCE,
    ),
    (
        None,
        'footer-services-events',
        urls.SERVICES_EVENTS,
    ),
    (
        'About',
        'footer-site-links-about',
        urls.ABOUT,
    ),
    (
        'Contact us',
        'footer-site-links-contact',
        urls.CONTACT_US,
    ),
    (
        'Privacy and cookies',
        'footer-site-links-privacy-and-cookies',
        urls.PRIVACY_AND_COOKIES,
    ),
    (
        'Terms and conditions',
        'footer-site-links-t-and-c',
        urls.TERMS_AND_CONDITIONS,
    ),
    (
        'Department for International Trade on GOV.UK',
        'footer-site-links-dit',
        urls.DIT
    )
))
def test_footer_ids_match_urls_and_text(
    title, element_id, url, settings
):
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    html = render_to_string(
        'directory_components/header_footer_old/footer.html', context
    )
    soup = BeautifulSoup(html, 'html.parser')

    element = soup.find(id=element_id)
    assert element.attrs['href'] == url
    if title:
        assert element.string == title


@pytest.mark.parametrize('title,element_id,url', (
    (
        'Contact us',
        'footer-contact',
        urls.CONTACT_US,
    ),
    (
        'Privacy and cookies',
        'footer-privacy-and-cookies',
        urls.PRIVACY_AND_COOKIES,
    ),
    (
        'Terms and conditions',
        'footer-terms-and-conditions',
        urls.TERMS_AND_CONDITIONS,
    ),
    (
        'Department for International Trade on GOV.UK',
        'footer-dit',
        urls.DIT
    ),
    (
        'Go to the page for international businesses',
        'footer-international',
        urls.GREAT_INTERNATIONAL
    ),
))
def test_domestic_footer_v2_ids_match_urls_and_text(
    title, element_id, url, settings
):
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    html = render_to_string(
        'directory_components/header_footer/domestic_footer.html', context
    )
    soup = BeautifulSoup(html, 'html.parser')

    element = soup.find(id=element_id)
    assert element.attrs['href'] == url
    if title:
        assert element.string == title


@pytest.mark.parametrize('title,element_id,url', (
    (
        'Contact us',
        'footer-contact',
        urls.CONTACT_US,
    ),
    (
        'Privacy and cookies',
        'footer-privacy-and-cookies',
        urls.PRIVACY_AND_COOKIES,
    ),
    (
        'Terms and conditions',
        'footer-terms-and-conditions',
        urls.TERMS_AND_CONDITIONS,
    ),
    (
        'Department for International Trade on GOV.UK',
        'footer-dit',
        urls.DIT
    ),
    (
        'Go to the page for UK businesses',
        'footer-domestic',
        urls.SERVICES_GREAT_DOMESTIC
    ),
))
def test_international_footer_v2_ids_match_urls_and_text(
    title, element_id, url, settings
):
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    html = render_to_string(
        'directory_components/header_footer/international_footer.html',
        context
    )
    soup = BeautifulSoup(html, 'html.parser')

    element = soup.find(id=element_id)
    assert element.attrs['href'] == url
    if title:
        assert element.string == title


@pytest.mark.parametrize('template, link_id', (
    (
        'directory_components/header_footer_old/header.html',
        'header-services-market-access'
    ),
    (
        'directory_components/header_footer_old/footer.html',
        'footer-services-market-access'
    )
))
@pytest.mark.parametrize('feature_status', [True, False])
def test_market_access_journey_feature_flag_shows_and_hides_links(
    template, link_id, feature_status,
):
    context = {
        **context_processors.header_footer_processor(None),
        'features': {'MARKET_ACCESS_ON': feature_status}
    }
    html = render_to_string(template, context)
    soup = BeautifulSoup(html, 'html.parser')

    if feature_status is True:
        assert not soup.find(id=link_id) is False
        assert soup.find(
            id=link_id
        ).attrs['href'] == urls.build_great_url('report-trade-barrier/')
    else:
        assert not soup.find(id=link_id) is True


@pytest.mark.parametrize('feature_status', [True, False])
def test_service_header_adjusted_width_according_to_market_access_feature(
    feature_status
):
    context = {
        **context_processors.header_footer_processor(None),
        'features': {'MARKET_ACCESS_ON': feature_status}
    }
    html = render_to_string(
        'directory_components/header_footer_old/header.html',
        context
    )
    soup = BeautifulSoup(html, 'html.parser')

    if feature_status is True:
        assert 'column-sixth' in soup.find(
            id='services-links-list'
        ).findChildren('li', recursive=False)[0].attrs['class']
    else:
        assert 'column-fifth' in soup.find(
            id='services-links-list'
        ).findChildren('li', recursive=False)[0].attrs['class']


@pytest.mark.parametrize('template_name,type', (
    ('directory_components/header_footer/header.html', 'header'),
    ('directory_components/header_footer/footer.html', 'footer'),
))
def test_new_header_footer_feature_flag_on(template_name, type, settings):
    context = {
        'features': {'NEW_HEADER_FOOTER_ON': True}
    }

    html = render_to_string(template_name, context)

    soup = BeautifulSoup(html, 'html.parser')

    assert soup.find(id='great-global-{}-logo'.format(type))


@pytest.mark.parametrize('template_name,type', (
    ('directory_components/header_footer/header.html', 'header'),
    ('directory_components/header_footer/footer.html', 'footer'),
))
def test_new_header_footer_feature_flag_off(template_name, type, settings):
    context = {
        'features': {'NEW_HEADER_FOOTER_ON': False}
    }
    html = render_to_string(template_name, context)

    soup = BeautifulSoup(html, 'html.parser')

    assert soup.find(id='{}-dit-logo'.format(type))
