from django.conf import settings
import yaml
import pathlib

__here__ = pathlib.Path(__file__).parent

with open(__here__/"header_footer_urls.yml") as f:
    urls = yaml.load(f)


def analytics(request):
    return {
        'directory_components_analytics': {
            'GOOGLE_TAG_MANAGER_ID': settings.GOOGLE_TAG_MANAGER_ID,
            'GOOGLE_TAG_MANAGER_ENV': settings.GOOGLE_TAG_MANAGER_ENV,
            'UTM_COOKIE_DOMAIN': settings.UTM_COOKIE_DOMAIN,
        }
    }


def header_footer_urls(request):
    return {
        'header_footer_urls': urls
    }
