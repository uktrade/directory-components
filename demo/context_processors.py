from django.conf import settings
from urllib.parse import urljoin


def local_styles_processor(request):
    return {
        'use_local_styles': settings.USE_LOCAL_STYLES,
        'elements_local_url': urljoin(
            settings.LOCAL_STYLES_URL,
            'public/stylesheets/govuk-elements-styles.css'),
        'components_local_url': urljoin(
            settings.LOCAL_STYLES_URL,
            'public/stylesheets/elements-components.css'),
    }
