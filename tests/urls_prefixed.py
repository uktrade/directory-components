from django.urls import re_path, include

import tests.urls


urlpatterns = [
    re_path(
        r'^components/',
        include(tests.urls.urlpatterns)
    )
]
