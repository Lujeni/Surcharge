# -*- coding: utf-8 -*-

from collections import defaultdict
from urlparse import urlparse, urlunparse
from socket import gethostbyname
from textwrap import dedent
from time import time

import requests
from progressbar import ProgressBar
from gevent import Timeout, sleep as g_sleep
from gevent.pool import Pool

from surcharge import logger


__all__ = ['Surcharger']


class Surcharger(object):

    http_method_supported = ('get', 'post',)

    def __init__(self, url=None, method='get', concurrency=1, numbers=1,
                 duration=0, format='json', cli=False, **options):
        """
        Init all necessary stuff to make a benchmark

        :param url: URL that you want benchmark
        :param method: HTTP method
        :param concurrency: simulate *client* connection
        :param numbers: number of requests
        :param duration: duration in seconds. Override the numbers option.
        :param format: format for the benchmark result
        :param cli: Surcharge from the CLI (display some informations)
        :param options: *requests* options
        """
        self.url = url
        self.method = method
        self.concurrency = concurrency
        self.numbers = numbers
        self.duration = duration
        self.format = format
        self.cli = cli
        self.options = options

    def __call__(self):
        """
        Launch the benchmark.
        """
        logger.info("launch benchmark :: {}".format(self.__dict__()))

        self.result = []
        self.result = defaultdict(list)
        progress = ProgressBar()

        pool = Pool(self.concurrency)
        start = time()

        if self.duration:
            try:
                with Timeout(self.duration, False):
                    while True:
                        pool.spawn(self.surcharge)
                        g_sleep()
            except Timeout:
                pool.join()

        else:
            if self.cli:
                self.display_informations()
                range_numbers = progress(xrange(self.numbers))
            else:
                range_numbers = xrange(self.numbers)

            for number in range_numbers:
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
        try:
            start = time()
            response = getattr(requests, self.method)(self.url, **self.options)
            status_code = response.status_code
        except Exception as e:
            logger.error("error surcharge :: {}".format(e))
            status_code = 666
        finally:
            self.result[status_code].append(time() - start)

    def display_informations(self):
        """ Displays useful informations.
        """
        res = requests.head(self.url)
        print '\nServer: {server}\n'.format(**res.headers)
        print 'URL: {}\n'.format(self.url)
        print 'Concurrency level: {}\n'.format(self.concurrency)
        print 'Options: {}\n\n'.format(self.options)


class SurchargerStats(object):

    def __init__(self, surcharger):
        self.surcharger = surcharger
        self.result = self.surcharger.result

    def __call__(self):
        self.compute()
        self.send()

    def compute(self):
        try:
            self.stats = {
                'exec_time': self.surcharger.exec_time,
                'total': sum([len(self.result[key]) for key in self.result.iterkeys()]),
                'total_success': len(self.result[200]),
                'requests_process': 0,
                'min': 0,
                'max': 0,
                'moy': 0,
                'RPS': 0,
            }

            if self.stats['total_success']:
                request_process = sum(self.result[200])
                self.stats.update({
                    'requests_process': request_process,
                    'min': min(self.result[200]),
                    'max': max(self.result[200]),
                    'moy': request_process / self.stats['total_success'],
                    'RPS': self.stats['total_success'] / request_process * self.surcharger.concurrency,
                })

            self.stats['total_failed'] = self.stats['total'] - self.stats['total_success']
        except Exception as error:
            logger.error("compute stats :: {}".format(error))

    def stdout(self):
        print dedent('''\n
            Number process requests: {total}
            Time taken for tests: {exec_time:.2f}
            Complete requests: {total_success}
            Failed requests: {total_failed}
            Faster request: {min:.3f}
            Slower request: {max:.3f}
            Time per request (only success): {moy:.3f}
            Request per second: {RPS:.2f}
        '''.format(**self.stats))

    def send(self):
        if self.surcharger.cli:
            self.stdout()
