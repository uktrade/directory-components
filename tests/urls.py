from django.conf.urls import include, url
from django.views import View
from django.views.generic.base import RedirectView

import directory_components.views


admin_urls = [
    url(
        r"^thing/$",
        RedirectView.as_view(url='/login/'),
        name='thing'
    ),
]

urlpatterns = [
    url(
        r'^$',
        View.as_view(),
        name='index',
    ),
    url(
        r'^admin/',
        include(admin_urls, namespace='admin', app_name='admin')
    ),
    url(
        r"^robots\.txt$",
        directory_components.views.RobotsView.as_view(),
        name='robots'
    ),
    url(
        r"^sitemap\.txt$",
        View.as_view(),
        name='sitemap'
    ),
    url(
        r"^some/path/$",
        View.as_view(),
        name='some-path'
    ),
]
