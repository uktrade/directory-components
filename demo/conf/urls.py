from django.urls import re_path

from demo import views

urlpatterns = [
    re_path(
        r'^$',
        views.IndexPageView.as_view(),
        {'template_name': 'demo/index.html'},
        name='index',
    ),
    re_path(
        r'^404/$',
        views.Trigger404View.as_view(),
        name='404',
    ),
    re_path(
        r'^500/$',
        views.Trigger500ErrorView.as_view(),
        name='500',
    ),
    re_path(
        r'^great-domestic-header-footer/$',
        views.DomesticHeaderFooterView.as_view(),
        name='great-domestic-header-footer',
    ),
    re_path(
        r'^elements/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/elements.html'},
        name='elements',
    ),
    re_path(
        r'^details-accordions/$',
        views.DetailsView.as_view(),
        {'template_name': 'demo/details-accordions.html'},
        name='details-accordions',
    ),
    re_path(
        r'^key-facts/$',
        views.KeyFactsView.as_view(),
        {'template_name': 'demo/key-facts.html'},
        name='key-facts',
    ),
    re_path(
        r'^featured-articles/$',
        views.FeaturedArticlesView.as_view(),
        {'template_name': 'demo/featured-articles.html'},
        name='featured-articles',
    ),
    re_path(
        r'^statistics/$',
        views.DemoStatsView.as_view(),
        {'template_name': 'demo/statistics.html'},
        name='statistics',
    ),
    re_path(
        r'^widgets/$',
        views.DemoFormView.as_view(),
        name='widgets',
    ),
    re_path(
        r'^form-errors/$',
        views.DemoFormErrorsView.as_view(),
        name='form-errors',
    ),
    re_path(
        r'^components/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/components.html'},
        name='components',
    ),
    re_path(
        r'^buttons/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/buttons.html'},
        name='buttons',
    ),
    re_path(
        r'^full-width-banners/$',
        views.FullWidthBannersView.as_view(),
        {'template_name': 'demo/full-width-banners.html'},
        name='full-width-banners',
    ),
    re_path(
        r'^banners/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/banners.html'},
        name='banners',
    ),
    re_path(
        r'^message-boxes/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/message-boxes.html'},
        name='message-boxes',
    ),
    re_path(
        r'^cards/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/cards.html'},
        name='cards',
    ),
    re_path(
        r'^breadcrumbs/$',
        views.BreadcrumbsDemoPageView.as_view(),
        {'template_name': 'demo/breadcrumbs.html'},
        name='breadcrumbs',
    ),
    re_path(
        r'^search-page-components/$',
        views.SearchPageComponentsDemoPageView.as_view(),
        {'template_name': 'demo/search-page-components.html'},
        name='search-page-components',
    ),
    re_path(
        r'^fact-sheet/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/fact-sheet.html'},
        name='fact-sheet',
    ),
    re_path(
        r'^responsive/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/responsive.html'},
        name='responsive',
    ),
    re_path(
        r'^template-tags/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/cms.html'},
        name='cms-tags',
    ),
    re_path(
        r'^great-international-header-footer/$',
        views.InternationalHeaderView.as_view(),
        {'template_name': 'demo/great-international-header-footer.html'},
        name='great-international-header-footer',
    ),
    re_path(
        r'^invest-header/$',
        views.InvestHeaderView.as_view(),
        {'template_name': 'demo/invest-header.html'},
        name='invest-header',
    ),
    re_path(
        r'^google-tag-manager/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/google-tag-manager.html'},
        name='google-tag-manager',
    ),
    re_path(
        r'^pagination/$',
        views.DemoPaginationView.as_view(),
        name='pagination',
    ),
    re_path(
        r'^error-pages/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/error-pages.html'},
        name='error-pages'
    ),
    re_path(
        r'^react-components/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/react-components.html'},
        name='react-components'
    )
]

handler404 = 'directory_components.views.handler404'

handler500 = 'directory_components.views.handler500'
