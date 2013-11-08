# -*- coding: utf-8 -*-

from collections import namedtuple
from urlparse import urlparse, urlunparse
from socket import gethostbyname


Url = namedtuple('Url', 'fqn resolv')


# TODO: use a exceptions file
class MissingOption(Exception):
    pass


class BadOption(Exception):
    pass


class Surcharger(object):

    def __init__(self, url=None, method=None, concurrency=None, numbers=None, **options):
        self.url = url

    def __call__(self):
        pass

    @property
    def url(self):
        return u'{}'.format(getattr(self._url, 'fqn', self._url))

    @url.setter
    def url(self, value):
        """
        Resolving the URL because is a heavy process.
        We don't need that each request makes a DNS resolve.

        :param value: contains the URL
        :type value: str
        """
        if not value:
            raise MissingOption(u'URL is missing')

        url_result = urlparse(value)
        url_netloc = url_result.netloc.rsplit(':')

        if len(url_netloc) == 1:
            url_netloc.append('80')

        url_resolved = gethostbyname(url_netloc[0])
        url_full = url_resolved + ':' + url_netloc[1]
        new_url = urlunparse((url_result.scheme, url_full) + url_result[2:])

        self._url = Url(value, new_url)
