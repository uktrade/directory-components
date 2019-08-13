from collections import namedtuple
from django.utils import translation
from directory_constants import urls

HeaderLink = namedtuple('Page', 'name title url')


ABOUT_THE_UK = HeaderLink(
    name='about-the-uk',
    title=translation.gettext('About the UK'),
    url='/international/content/about-uk/'
)
WHY_THE_UK = HeaderLink(
    name='why-the-uk',
    title=translation.gettext('Why choose the UK'),
    url='/international/content/about-uk/why-choose-uk/'
)
INDUSTRIES = HeaderLink(
    name='industries',
    title=translation.gettext('Industries'),
    url=urls.GREAT_INTERNATIONAL_INDUSTRIES
)
REGIONS = HeaderLink(
    name='regions',
    title=translation.gettext('Regions'),
    url='/international/content/about-uk/regions'
)
CONTACT_INTERNATIONAL_TRIAGE = HeaderLink(
    name='contact',
    title=translation.gettext('Contact us'),
    url=urls.GREAT_INTERNATIONAL_CONTACT_US
)
EXPAND = HeaderLink(
    name='expand',
    title=translation.gettext('Expand to the UK'),
    url=urls.SERVICES_INVEST
)
HOW_TO_EXPAND = HeaderLink(
    name='how-to-expand',
    title=translation.gettext('How to expand to the UK'),
    url=urls.GREAT_INTERNATIONAL_HOW_TO_SETUP_IN_THE_UK
)
ISD = HeaderLink(
    name='investment-support-directory',
    title=translation.gettext('Professional advice'),
    url=urls.SERVICES_ISD
)
WHAT_WE_DO_EXPAND = HeaderLink(
    name='what-we-do',
    title=translation.gettext('How we help'),
    url=urls.GREAT_INTERNATIONAL_ABOUT_DIT + 'how-we-help-expand/'
)
CONTACT_EXPAND = HeaderLink(
    name='contact',
    title=translation.gettext('Contact Us'),
    url=urls.INVEST_CONTACT_US
)
INVEST = HeaderLink(
    name='invest',
    title=translation.gettext('Invest capital in the UK'),
    url=urls.GREAT_INTERNATIONAL_CAPITAL_INVEST_LANDING_PAGE
)
INVESTMENT_TYPES = HeaderLink(
    name='investment-types',
    title=translation.gettext('Investment types'),
    url='/international/content/investment-types/'
)
INVESTMENT_OPPORTUNITIES = HeaderLink(
    name='investment-opportunities',
    title=translation.gettext('Investment opportunities'),
    url='/international/content/opportunities/',
)
HOW_TO_INVEST_CAPITAL = HeaderLink(
    name='how-to-invest-capital',
    title=translation.gettext('How to invest capital'),
    url='/international/content/how-to-invest-capital/',
)
WHAT_WE_DO_INVEST = HeaderLink(
    name='what-we-do',
    title=translation.gettext('How we help'),
    url='/international/content/about-dit/how-we-help-invest-capital/',
)
CONTACT_INVEST = HeaderLink(
    name='contact',
    title=translation.gettext('Contact Us'),
    url='/international/content/capital-invest/contact/',
)
FAS = HeaderLink(
    name='trade',
    title=translation.gettext('Buy from the UK'),
    url=urls.SERVICES_FAS,
)
HOW_TO_BUY = HeaderLink(
    name='how-to-buy',
    title=translation.gettext('How to buy from the UK'),
    url='/international/content/how-to-buy/',
)
WHAT_WE_DO_TRADE = HeaderLink(
    name='what-we-do',
    title=translation.gettext('How we help'),
    url='/international/content/about-dit/how-we-help-trade/',
)
CONTACT_TRADE = HeaderLink(
    name='contact',
    title=translation.gettext('Contact Us'),
    url=urls.CONTACT_US
)
OVERVIEW_ABOUT = HeaderLink(
    name='overview',
    title=translation.gettext('Overview'),
    url='/international/content/about-uk/',
)
OVERVIEW_EXPAND = HeaderLink(
    name='overview',
    title=translation.gettext('Overview'),
    url=urls.SERVICES_FAS,
)
OVERVIEW_INVEST = HeaderLink(
    name='overview',
    title=translation.gettext('Overview'),
    url=urls.GREAT_INTERNATIONAL_CAPITAL_INVEST_LANDING_PAGE,
)
ABOUT_DIT = HeaderLink(
    name='about-dit',
    title=translation.gettext('About us'),
    url='/international/content/about-dit',
)