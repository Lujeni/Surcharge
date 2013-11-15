# -*- coding: utf-8 -*-

from collections import namedtuple
from urlparse import urlparse, urlunparse
from socket import gethostbyname
from time import time

# EXT
import requests
from gevent.pool import Pool

# SURCHARGE
from _exceptions import BadOption, MissingOption, MissingResult
from serializer import MixinSerializer

Url = namedtuple('Url', 'fqn addr')
Format = namedtuple('Format', 'name function')
HttpMethod = namedtuple('HttpMethod', 'name function')
HttpRequest = namedtuple('HttpRequest', 'status_code exec_time')


class Surcharger(MixinSerializer):

    http_method_supported = ('GET', 'POST',)

    def surcharge(self):
        """
        Make the request. Keep the status code of the response and
        the exec time in a result list.
        """
        start = time()
        response = self._method.function(self.url, **self.options)
        self.result.append(HttpRequest(response.status_code, time() - start))

    def __init__(self, url=None, method='get', concurrency=1, numbers=1, format='json', **options):
        """
        Init all necessary stuff for make a benchmark

        :param url: URL that you want benchmark
        :param method: HTTP method
        :param concurrency: simulate *client* connection
        :param numbers: number of requests
        :param format: format for the benchmark result
        :param options: *requests* options
        """
        self.url = url
        self.method = method
        self.concurrency = concurrency
        self.numbers = numbers
        self.format = format
        self.options = options

    def __call__(self):
        """
        Launch the benchmark.
        """
        self.result = []
        pool = Pool(self.concurrency)

        for request in xrange(self.numbers):
            pool.spawn(self.surcharge)
            pool.join()

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
                value.upper(), self.http_method_supported))

        self._method = HttpMethod(value.upper(), getattr(requests, value.lower()))

    @property
    def format(self):
        return u'{}'.format(getattr(self._format, 'name', None))

    @format.setter
    def format(self, value):
        """
        See serializer.py for format supported

        :param value: format
        :type value: str
        :example value: json
        """
        if not value:
            raise MissingOption(u'Format is missing')

        _format = getattr(self, '_{}'.format(value.lower()), None)
        if not _format:
            raise BadOption(u'Unknown Format ({} not supported)'.format(value.upper()))

        self._format = Format(value.lower(), _format)

    def retrieve_result(self):
        """
        Retrieve the benchmark result in the
        specify format
        """
        if not self.result:
            raise MissingResult(u'Ensure that the benchmark was launched')
        else:
            return self._format.function(self.result)
