# -*- coding: utf-8 -*-

from collections import namedtuple
from urlparse import urlparse, urlunparse
from socket import gethostbyname

import requests

Url = namedtuple('Url', 'fqn addr')
HttpMethod = namedtuple('HttpMethod', 'name function')


# TODO: use a exceptions file
class MissingOption(Exception):
    pass


class BadOption(Exception):
    pass


class Surcharger(object):

    http_method_supported = ('GET', 'POST',)

    def __init__(self, url=None, method='get', concurrency=1, numbers=1, **options):
        """
        Init all necessary stuff for make a benchmark

        :param url: URL that you want benchmark
        :param method: HTTP method
        :param concurrency: simulate *client* connection
        :param numbers: number of requests
        :param options: *requests* options
        """
        self.url = url
        self.method = method
        self.concurrency = concurrency
        self.numbers = numbers
        self.options = options

    def __call__(self):
        pass

    def __repr__(self):
        return u'{}'.format('')

    def __dict__(self):
        return dict(
            url=self.url,
            method=self.method,
            concurrency=self.concurrency,
            numbers=self.numbers,
            options=self.options
        )

    @property
    def url(self):
        return u'{}'.format(getattr(self._url, 'fqn', None))

    @url.setter
    def url(self, value):
        """
        Resolving the URL because is a heavy process
        We don't need that each request makes a DNS resolve

        :param value: contains the URL
        :type value: str
        :example value: 'http://google.com'
        """

        if not value:
            raise MissingOption(u'URL is missing')

        url_result = urlparse(value)
        if not url_result.scheme:
            raise BadOption(u'URL scheme is missing')

        url_netloc = url_result.netloc.rsplit(':')

        if len(url_netloc) == 1:
            url_netloc.append('80')

        url_resolved = gethostbyname(url_netloc[0])
        url_full = url_resolved + ':' + url_netloc[1]
        new_url = urlunparse((url_result.scheme, url_full) + url_result[2:])

        self._url = Url(value, new_url)

    @property
    def method(self):
        return u'{}'.format(getattr(self._method, 'name', None))

    @method.setter
    def method(self, value):
        """
        Support *requests* HTTP method

        :param value: HTTP method
        :type value: str
        :example value: get
        """
        if not value:
            raise MissingOption(u'HTTP method is missing')

        if not value.upper() in self.http_method_supported:
            raise BadOption(u'Unknown HTTP method ({} not in {})'.format(
                value.upper()), self.http_method_supported)

        self._method = HttpMethod(value.upper(), getattr(requests, value.lower()))
