from django.conf import settings
from django.views.generic import TemplateView


class RobotsView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            FEATURE_SEARCH_ENGINE_INDEXING_DISABLED=(
                settings.FEATURE_SEARCH_ENGINE_INDEXING_DISABLED
            ),
            **kwargs
        )
