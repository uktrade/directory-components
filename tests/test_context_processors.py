from directory_components import context_processors


def test_analytics(settings):
    settings.GOOGLE_TAG_MANAGER_ID = '123'
    settings.GOOGLE_TAG_MANAGER_ENV = '?thing=1'
    settings.UTM_COOKIE_DOMAIN = '.thing.com'

    actual = context_processors.analytics(None)

    assert actual == {
        'analytics': {
            'GOOGLE_TAG_MANAGER_ID': '123',
            'GOOGLE_TAG_MANAGER_ENV': '?thing=1',
            'UTM_COOKIE_DOMAIN': '.thing.com',
        }
    }


def test_external_service_urls(settings):
    settings.EXTERNAL_SERVICE_FEEDBACK_URL = 'http://example.com/feedback'

    actual = context_processors.external_service_urls(None)

    assert actual == {
        'external_services': {
            'FEEDBACK_URL': 'http://example.com/feedback',
        }
    }


def test_analytics_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'core.context_processors.analytics' in processors


def test_external_service_urls_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'core.context_processors.external_service_urls' in processors
