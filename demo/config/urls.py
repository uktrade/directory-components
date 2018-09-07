from django.conf.urls import url

from demo import views

urlpatterns = [
    url(
        r'^$',
        views.HelloWorld.as_view(),
        name='hello-world',
    ),
    url(
        r'^404/$',
        views.NotFound.as_view(),
        name='404',
    ),
    url(
        r'^widgets/$',
        views.DemoFormView.as_view(),
        name='widgets',
    ),
    url(
        r'^components/$',
        views.ComponentsView.as_view(),
        name='components',
    ),
    url(
        r'^responsive-grid/$',
        views.ResponsiveGridView.as_view(),
        name='responsive-grid',
    ),
    url(
        r'^invest/$',
        views.InvestHeaderFooterView.as_view(),
        name='invest-header-footer',
    ),
    url(
        r'^prototype/prototype-article$',
        views.PrototypeArticlePageView.as_view(),
        name='prototype-article',
    ),
    url(
        r'^prototype/prototype-guidance-list$',
        views.PrototypeGuidanceListView.as_view(),
        name='prototype-guidance-list',
    ),
    url(
        r'^template-tags/$',
        views.TemplateTagsView.as_view(),
        name='template-tags',
    ),
]
