import urllib.parse
from collections import namedtuple

from ipware.ip2 import get_client_ip
from mohawk import Receiver
from mohawk.exc import HawkFail

from django.conf import settings
from django.utils.encoding import iri_to_uri

from directory_components import constants


IPs = namedtuple('IPs', ['second', 'third'])


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
        return urllib.parse.urljoin(
            self.prefix, self.request.path.lstrip('/')
        )

    @property
    def full_path(self):
        path = self.path
        if not path.endswith('/'):
            path += '/'
        querystring = self.request.META.get('QUERY_STRING', '')
        if querystring:
            path += ('?' + iri_to_uri(querystring))
        return path


class IpwareRemoteIPAddressRetriver:
    MESSAGE_NOT_FOUND = 'IP not found'
    MESSAGE_UNROUTABLE = 'IP is private'

    @classmethod
    def get_ip_address(cls, request):
        client_ip, is_routable = get_client_ip(request)
        if not client_ip:
            raise LookupError(cls.MESSAGE_NOT_FOUND)
        if not is_routable:
            raise LookupError(cls.MESSAGE_UNROUTABLE)
        return client_ip


class GovukPaaSRemoteIPAddressRetriver:
    MESSAGE_MISSING_HEADER = 'X-Forwarded-For not in HTTP headers'
    MESSAGE_INVALID_IP_COUNT = 'Not enough IP addresses in X-Forwarded-For'

    @classmethod
    def get_ip_address(cls, request):
        """
        Returns the second AND third FROM THE RIGHT
        IP addresses of the client making a HTTP request, using the
        second-to-last IP address in the X-Forwarded-For header. This
        should not be able to be spoofed in GovukPaaS, but it is not
        safe to use in other environments.

        Args:
            request (HttpRequest): the incoming Django request object

        Returns:
            str: The IP address of the incoming request

        Raises:
            LookupError: The X-Forwarded-For header is not present, or
            does not contain enough IPs
        """
        if 'HTTP_X_FORWARDED_FOR' not in request.META:
            raise LookupError(cls.MESSAGE_MISSING_HEADER)

        x_forwarded_for = request.META['HTTP_X_FORWARDED_FOR']
        ip_addesses = x_forwarded_for.split(',')
        if len(ip_addesses) < 2:
            raise LookupError(cls.MESSAGE_INVALID_IP_COUNT)

        if len(ip_addesses) >= 3:
            ips = IPs(ip_addesses[-2].strip(), ip_addesses[-3].strip())
        else:
            ips = IPs(ip_addesses[-2].strip(), None)
        return ips


class RemoteIPAddressRetriever:
    """
    Different environments retrieve the remote IP address differently. This
    class negotiates that.

    """

    @classmethod
    def __new__(cls, *args, **kwargs):
        value = getattr(
            settings,
            'IP_RESTRICTOR_REMOTE_IP_ADDRESS_RETRIEVER',
            constants.IP_RETRIEVER_NAME_GOV_UK
        )
        if value == constants.IP_RETRIEVER_NAME_GOV_UK:
            return GovukPaaSRemoteIPAddressRetriver()
        elif value == constants.IP_RETRIEVER_NAME_IPWARE:
            return IpwareRemoteIPAddressRetriver()
        raise NotImplementedError()


def is_skip_ip_check_signature_valid(signature):
    if not getattr(settings, 'IP_RESTRICTOR_SKIP_CHECK_ENABLED', False):
        return False

    credentials = {
        'id': settings.IP_RESTRICTOR_SKIP_CHECK_SENDER_ID,
        'key': settings.IP_RESTRICTOR_SKIP_CHECK_SECRET,
        'algorithm': 'sha256'
    }
    try:
        Receiver(
            lambda x: credentials,
            signature,
            '/',
            '',
            accept_untrusted_content=True
        )
    except HawkFail:
        return False
    else:
        return True
