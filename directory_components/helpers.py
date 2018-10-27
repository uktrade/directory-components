import urllib.parse

from django.utils.encoding import iri_to_uri


def add_next(destination_url, current_url):
    if 'next=' in destination_url:
        return destination_url
    concatenation_character = '&' if '?' in destination_url else '?'
    return '{url}{concatenation_character}next={next}'.format(
        url=destination_url,
        concatenation_character=concatenation_character,
        next=current_url,
    )


class SocialLinkBuilder:
    templates = (
        ('email', 'mailto:?body={url}&subject={body}'),
        ('twitter', 'https://twitter.com/intent/tweet?text={body}{url}'),
        ('facebook', 'https://www.facebook.com/share.php?u={url}'),
        (
            'linkedin',
            (
                'https://www.linkedin.com/shareArticle'
                '?mini=true&url={url}&title={body}&source=LinkedIn'
            )
        )
    )

    def __init__(self, url, page_title, app_title):
        self.url = url
        self.page_title = page_title
        self.app_title = app_title

    @property
    def body(self):
        body = '{app_title} - {page_title} '.format(
            app_title=self.app_title, page_title=self.page_title
        )
        return urllib.parse.quote(body)

    @property
    def links(self):
        return {
            name: template.format(url=self.url, body=self.body)
            for name, template in self.templates
        }


class UrlPrefixer:

    def __init__(self, request, prefix):
        self.prefix = prefix
        self.request = request

    @property
    def is_path_prefixed(self):
        return self.request.path.startswith(self.prefix)

    @property
    def path(self):
        canonical_path = urllib.parse.urljoin(
            self.prefix, self.request.path.lstrip('/')
        )
        if not canonical_path.endswith('/'):
            canonical_path += '/'
        return canonical_path

    @property
    def full_path(self):
        path = self.path
        querystring = self.request.META.get('QUERY_STRING', '')
        if querystring:
            path += ('?' + iri_to_uri(querystring))
        return path
