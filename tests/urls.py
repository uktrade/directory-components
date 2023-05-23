from django.urls import include, re_path
from django.views import View
from django.views.generic.base import RedirectView

import directory_components.views
import demo.views


admin_urls = [
    re_path(
        r"^thing/$",
        RedirectView.as_view(url='/login/'),
        name='thing'
    ),
]

urlpatterns = [
    re_path(
        r'^$',
        View.as_view(),
        name='index',
    ),
    re_path(r'^admin/', include(admin_urls)),
    re_path(
        r"^robots\.txt$",
        directory_components.views.RobotsView.as_view(),
        name='robots'
    ),
    re_path(
        r'^404/$',
        demo.views.Trigger404View.as_view(),
        name='404',
    ),
    re_path(
        r'^500/$',
        demo.views.Trigger500ErrorView.as_view(),
        name='500',
    ),
    re_path(
        r"^sitemap\.txt$",
        View.as_view(),
        name='sitemap'
    ),
    re_path(
        r"^some/path/$",
        View.as_view(),
        name='some-path'
    ),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
]

handler404 = 'directory_components.views.handler404'

handler500 = 'directory_components.views.handler500'
