# -*- coding: utf-8 -*-
import sys

from collections import defaultdict
from urlparse import urlparse, urlunparse
from socket import gethostbyname
from time import time

import requests
from progressbar import ProgressBar
from gevent.pool import Pool

from surcharge import logger


__all__ = ['Surcharger']


class Surcharger(object):

    http_method_supported = ('get', 'post',)

    def __init__(self, url=None, method='get', concurrency=1, numbers=1,
                 format='json', cli=False, **options):
        """
        Init all necessary stuff to make a benchmark

        :param url: URL that you want benchmark
        :param method: HTTP method
        :param concurrency: simulate *client* connection
        :param numbers: number of requests
        :param format: format for the benchmark result
        :param cli: Surcharge from the CLI (display some informations)
        :param options: *requests* options
        """
        self.url = url
        self.method = method
        self.concurrency = concurrency
        self.numbers = numbers
        self.format = format
        self.cli = cli
        self.options = options

    def __call__(self):
        """
        Launch the benchmark.
        """
        self.result = []
        self.result = defaultdict(list)
        progress = ProgressBar()

        if self.cli:
            self.display_informations()
            range_numbers = progress(xrange(self.numbers))
        else:
            range_numbers = xrange(self.numbers)

        start = time()
        pool = Pool(self.concurrency)
        for request in range_numbers:
            pool.spawn(self.surcharge)
        pool.join()

        self.exec_time = time() - start

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
        return u'{}'.format(self._url)

    @url.setter
    def url(self, value):
        """
        Resolving the URL is a heavy process.
        We don't need that each request makes a DNS resolve.
        """
        scheme, netloc, path, params, query, fragment = urlparse(value)

        if not scheme:
            mess = "Invalid URL {}: No schema supplied. Perhaps you meant http://{}?"
            raise Exception(mess.format(value, value))

        url_netloc = netloc.rsplit(':')
        if len(url_netloc) == 1:
            url_netloc.append('80')

        url_resolved = gethostbyname(url_netloc[0])
        url_full = url_resolved + ':' + url_netloc[1]
        self._url = urlunparse((scheme, url_full) + (path, params, query, fragment))

    @property
    def method(self):
        return u'{}'.format(self._method)

    @method.setter
    def method(self, value):
        """
        Ensure the HTTP method is supported.
        """
        if value.lower() not in self.http_method_supported:
            mess = "Invalid method {}: Not supported. Only {}"
            raise Exception(mess.format(value, self.http_method_supported))

        self._method = value.lower()

    def surcharge(self):
        """
        Make the request. Keep the status code of the response and
        the exec time in a result list.
        """
        start = time()
        response = getattr(requests, self.method)(self.url, **self.options)
        self.result[response.status_code].append(time() - start)

    def display_informations(self):
        """ Displays useful informations.
        """
        res = requests.head(self.url)
        sys.stdout.write('\nServer: %(server)s\n' % res.headers)
        sys.stdout.write('URL: {}\n'.format(self.url))
        sys.stdout.write('Concurrency level: {}\n'.format(self.concurrency))
        sys.stdout.write('Options: {}\n\n'.format(self.options))


class SurchargerStats(object):

    def __init__(self, surcharger):
        self.surcharger = surcharger
        self.result = self.surcharger.result

    def __call__(self):
        self.compute()
        self.send()

    def compute(self):
        try:
            self.total = sum([len(self.result[key]) for key in self.result.iterkeys()])
            self.total_success = len(self.result[200])
            if self.total_success:
                self.requests_process = sum(self.result[200])
                self.min = min(self.result[200])
                self.max = max(self.result[200])
                self.moy = self.requests_process / self.total_success
                self.RPS = self.total_success / self.requests_process * self.surcharger.concurrency
            else:
                self.requests_process = 0
                self.min = 0
                self.max = 0
                self.moy = 0
                self.RPS = 0
            self.total_failed = self.total - self.total_success
        except Exception as error:
            logger.error("compute stats :: {}".format(error))

    def stdout(self):
        sys.stdout.write('\nNumber process requests: {}\n'.format(self.total))
        sys.stdout.write('Time taken for tests: {:.2f}\n\n'.format(self.surcharger.exec_time))
        sys.stdout.write('Complete requests: {}\n'.format(self.total_success))
        sys.stdout.write('Failed requests: {}\n\n'.format(self.total_failed))
        sys.stdout.write('Faster request: {:.3f}\n'.format(self.min))
        sys.stdout.write('Slower request: {:.3f}\n'.format(self.max))
        sys.stdout.write('Time per request (only success): {:.3f}\n'.format(self.moy))
        sys.stdout.write('Request per second: {:.2f}\n'.format(self.RPS))

    def send(self):
        if self.surcharger.cli:
            self.stdout()
