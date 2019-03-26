from django.conf.urls import url

from demo import views

urlpatterns = [
    url(
        r'^$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/index.html'},
        name='index',
    ),
    url(
        r'^404/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/404.html'},
        name='404',
    ),
    url(
        r'^great-international-header-footer/$',
        views.InternationalHeaderView.as_view(),
        {'template_name': 'demo/great-international-header-footer.html'},
        name='great-international-header-footer',
    ),
    url(
        r'^great-domestic-header-footer-search/$',
        views.GreatDomesticHeaderSearchView.as_view(),
        {'template_name': 'demo/great-domestic-header-footer.html'},
        name='great-domestic-header-footer-search',
    ),
    url(
        r'^great-domestic-header-footer/$',
        views.GreatDomesticHeaderView.as_view(),
        {'template_name': 'demo/great-domestic-header-footer.html'},
        name='great-domestic-header-footer',
    ),
    url(
        r'^old-domestic-header-footer/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/old-domestic-header-footer.html'},
        name='old-domestic-header-footer',
    ),
    url(
        r'^elements/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/elements.html'},
        name='elements',
    ),
    url(
        r'^widgets/$',
        views.DemoFormView.as_view(),
        name='widgets',
    ),
    url(
        r'^form-errors/$',
        views.DemoFormErrorsView.as_view(),
        name='form-errors',
    ),
    url(
        r'^components/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/components.html'},
        name='components',
    ),
    url(
        r'^buttons/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/buttons.html'},
        name='buttons',
    ),
    url(
        r'^hero-banner/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/hero-banner.html'},
        name='hero-banner',
    ),
    url(
        r'^banners/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/banners.html'},
        name='banners',
    ),
    url(
        r'^cards/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/cards.html'},
        name='cards',
    ),
    url(
        r'^responsive/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/responsive.html'},
        name='responsive',
    ),
    url(
        r'^invest/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/invest_header_footer.html'},
        name='invest-header-footer',
    ),
    url(
        r'^template-tags/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/template_tags.html'},
        name='template-tags',
    ),
]
