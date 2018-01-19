from directory_components import context_processors


def test_analytics(settings):
    settings.GOOGLE_TAG_MANAGER_ID = '123'
    settings.GOOGLE_TAG_MANAGER_ENV = '?thing=1'
    settings.UTM_COOKIE_DOMAIN = '.thing.com'

    actual = context_processors.analytics(None)

    assert actual == {
        'directory_components_analytics': {
            'GOOGLE_TAG_MANAGER_ID': '123',
            'GOOGLE_TAG_MANAGER_ENV': '?thing=1',
            'UTM_COOKIE_DOMAIN': '.thing.com',
        }
    }


def test_urls(settings):
    settings.EXTERNAL_SERVICE_FEEDBACK_URL = 'http://example.com/feedback'

    actual = context_processors.urls(None)

    assert actual == {
        'directory_components_urls': {
            'FEEDBACK_URL': 'http://example.com/feedback',
        }
    }
