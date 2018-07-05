from django.conf.urls import url
from django.views import View

import directory_components.views


urlpatterns = [
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
]
