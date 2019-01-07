from bs4 import BeautifulSoup
from directory_constants.constants import urls
import pytest

from django.template.loader import render_to_string

from directory_components import context_processors


@pytest.mark.parametrize('template_name', [
    'directory_components/header_footer/header.html',
    'directory_components/header_footer/footer.html',
    'directory_components/header_footer/header_static.html',
])
def test_templates_rendered(template_name):
    html = render_to_string(template_name)
    assert '<div' in html
    assert '<ul' in html
    assert '<a' in html


def test_header_logged_in():
    template_name = 'directory_components/header_footer/header.html'
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


def test_header_logged_out():
    template_name = 'directory_components/header_footer/header.html'
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
    urls.SERVICE_EXPORT_READINESS,
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
def test_urls_exist_in_header_export_journey_off(url, context, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None)
    }
    template_name = 'directory_components/header_footer/header.html'
    assert url in render_to_string(template_name, context)


@pytest.mark.parametrize('url', [
    urls.SERVICE_EXPORT_READINESS,
    urls.CUSTOM_PAGE,
    urls.EXPORTING_NEW,
    urls.EXPORTING_REGULAR,
    urls.EXPORTING_OCCASIONAL,
    urls.GUIDANCE_FINANCE,
    urls.GUIDANCE_GETTING_PAID,
    urls.GUIDANCE_MARKET_RESEARCH,
    urls.GUIDANCE_CUSTOMER_INSIGHT,
    urls.GUIDANCE_BUSINESS_PLANNING,
    urls.GUIDANCE_OPERATIONS_AND_COMPLIANCE,
    urls.SERVICES_EXOPPS,
    urls.GET_FINANCE,
])
def test_urls_exist_in_header_export_journey_on(url, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    template_name = 'directory_components/header_footer/header.html'
    assert url in render_to_string(template_name, context)


@pytest.mark.parametrize('url', [
    urls.SERVICE_EXPORT_READINESS,
    urls.CUSTOM_PAGE,
    urls.EXPORTING_NEW,
    urls.EXPORTING_REGULAR,
    urls.EXPORTING_OCCASIONAL,
    urls.GUIDANCE_FINANCE,
    urls.GUIDANCE_GETTING_PAID,
    urls.GUIDANCE_MARKET_RESEARCH,
    urls.GUIDANCE_CUSTOMER_INSIGHT,
    urls.GUIDANCE_BUSINESS_PLANNING,
    urls.GUIDANCE_OPERATIONS_AND_COMPLIANCE,
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
def test_urls_exist_in_footer_export_journey_on(url, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    template_name = 'directory_components/header_footer/footer.html'
    assert url in render_to_string(template_name, context)


@pytest.mark.parametrize('url', [
    urls.SERVICE_EXPORT_READINESS,
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
def test_urls_exist_in_footer_export_journey_off(url, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    template_name = 'directory_components/header_footer/footer.html'
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
def test_header_ids_match_urls_and_text_export_journey_off(
    title, element_id, url, settings
):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }

    html = render_to_string(
        'directory_components/header_footer/header.html', context
    )
    soup = BeautifulSoup(html, 'html.parser')

    element = soup.find(id=element_id)

    assert element.attrs['href'] == url
    if title:
        assert element.string == title


@pytest.mark.parametrize('title,element_id,url', (
    (
        'I\'m new to exporting',
        'header-export-readiness-new',
        urls.EXPORTING_NEW,
    ),
    (
        'I export occasionally',
        'header-export-readiness-occasional',
        urls.EXPORTING_OCCASIONAL,
    ),
    (
        'I\'m a regular exporter',
        'header-export-readiness-regular',
        urls.EXPORTING_REGULAR,
    ),
    (
        'Your export journey',
        'header-custom-page-link',
        urls.CUSTOM_PAGE,
    ),
    (
        'Market research',
        'header-guidance-market-research',
        urls.GUIDANCE_MARKET_RESEARCH,
    ),
    (
        'Customer insight',
        'header-guidance-customer-insight',
        urls.GUIDANCE_CUSTOMER_INSIGHT,
    ),
    (
        'Finance',
        'header-guidance-finance',
        urls.GUIDANCE_FINANCE,
    ),
    (
        'Business planning',
        'header-guidance-business-planning',
        urls.GUIDANCE_BUSINESS_PLANNING,
    ),
    (
        'Getting paid',
        'header-guidance-getting-paid',
        urls.GUIDANCE_GETTING_PAID,
    ),
    (
        'Operations and compliance',
        'header-guidance-operations-and-compliance',
        urls.GUIDANCE_OPERATIONS_AND_COMPLIANCE,
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
def test_header_ids_match_urls_and_text_export_journey_on(
    title, element_id, url, settings
):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    html = render_to_string(
        'directory_components/header_footer/header.html', context
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
def test_footer_ids_match_urls_and_text_export_journey_off(
    title, element_id, url, settings
):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    html = render_to_string(
        'directory_components/header_footer/footer.html', context
    )
    soup = BeautifulSoup(html, 'html.parser')

    element = soup.find(id=element_id)
    assert element.attrs['href'] == url
    if title:
        assert element.string == title


@pytest.mark.parametrize('title,element_id,url', (
    (
        'I\'m new to exporting',
        'footer-export-readiness-new',
        urls.EXPORTING_NEW,
    ),
    (
        'I export occasionally',
        'footer-export-readiness-occasional',
        urls.EXPORTING_OCCASIONAL,
    ),
    (
        'I\'m a regular exporter',
        'footer-export-readiness-regular',
        urls.EXPORTING_REGULAR,
    ),
    (
        'Your export journey',
        'footer-custom-page-link',
        urls.CUSTOM_PAGE,
    ),
    (
        'Market research',
        'footer-guidance-market-research',
        urls.GUIDANCE_MARKET_RESEARCH,
    ),
    (
        'Customer insight',
        'footer-guidance-customer-insight',
        urls.GUIDANCE_CUSTOMER_INSIGHT,
    ),
    (
        'Finance',
        'footer-guidance-finance',
        urls.GUIDANCE_FINANCE,
    ),
    (
        'Business planning',
        'footer-guidance-business-planning',
        urls.GUIDANCE_BUSINESS_PLANNING,
    ),
    (
        'Getting paid',
        'footer-guidance-getting-paid',
        urls.GUIDANCE_GETTING_PAID,
    ),
    (
        'Operations and compliance',
        'footer-guidance-operations-and-compliance',
        urls.GUIDANCE_OPERATIONS_AND_COMPLIANCE,
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
def test_footer_ids_match_urls_and_text_export_journey_on(
    title, element_id, url, settings
):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
    context = {
        **context_processors.header_footer_processor(None),
        **context_processors.urls_processor(None),
        **context_processors.feature_flags(None),
    }
    html = render_to_string(
        'directory_components/header_footer/footer.html', context
    )
    soup = BeautifulSoup(html, 'html.parser')

    element = soup.find(id=element_id)
    assert element.attrs['href'] == url
    if title:
        assert element.string == title


def test_header_export_journey_links():
    context = {
        'features': {'EXPORT_JOURNEY_OFF': True}
    }
    html = render_to_string(
        'directory_components/header_footer/header.html', context)

    soup = BeautifulSoup(html, 'html.parser')
    assert not soup.find(id='header-custom-page-link')
    assert not soup.find(id='export-readiness-links')
    assert not soup.find(id='header-export-readiness-new')
    assert not soup.find(id='header-export-readiness-regular')
    assert not soup.find(id='header-export-readiness-occasional')


def test_footer_export_journey_links():
    context = {
        'features': {'EXPORT_JOURNEY_OFF': True}
    }
    html = render_to_string(
        'directory_components/header_footer/footer.html', context)

    soup = BeautifulSoup(html, 'html.parser')
    assert not soup.find(id='footer-export-readiness-links')
    assert not soup.find(id='footer-export-readiness-new')
    assert not soup.find(id='footer-export-readiness-regular')
    assert not soup.find(id='footer-export-readiness-occasional')
