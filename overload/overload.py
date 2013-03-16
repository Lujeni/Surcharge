#/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

import time
import requests
import argparse
import gevent
import os
import sys

from gevent.pool import Pool
from collections import defaultdict
from sys import exit


HTTP_VERBS = 'GET', 'POST', 'PUT', 'DELETE'
_stats = defaultdict(list)


def progress(func):
    """
    @decorator:
        display an tiret for each query treatment
    """
    def wrapper(*args):
        sys.stdout.write('-')
        sys.stdout.flush()
        return func(*args)
    return wrapper


def cookies_parse(cookies):
    """
    @args:
        <list_of_cookies>

    @return:
        <dict_of_cookies>
    """
    _cookies = {}
    try:
        for cookie in cookies:
            _cookie = cookie.split(':')
            if len(_cookie) != 2:
                raise Exception
            else:
                _cookie = iter(reversed(_cookie))
                _cookies[_cookie.next()] = _cookie.next()
    except Exception:
        sys.stdout.write('discarding invalid cookies: {}\n'.format(cookie))
        exit(1)
    else:
        return _cookies


def clear_stats():
    """
    keeps consistent stats when --repeat is used
    """
    global _stats
    del _stats
    _stats = defaultdict(list)


# TODO: fix bug AttributeError: 'Greenlet' object has no attribute '_run'
@progress
def call(method, url, options):
    """
    @args:
        <method_of_request>
        <str_url>
        <dict_requests_options>

    made a request and updates the stats
    """
    try:
        start = time.time()
        res = method(url, **options)
        code = res.status_code
    except requests.exceptions.Timeout:
        code = 408
    except Exception:
        code = 404
    finally:
        _stats[code].append(time.time()-start)


class Overload(object):

    def __init__(self, url, method, concurrency, numbers, duration, **options):
        self.url = url
        self.method = method
        self.concurrency = concurrency
        self.numbers = numbers
        self.duration = duration
        self.options = options

    @property
    def informations(self):
        res = requests.head(self.url)
        sys.stdout.write('\nServer: %(server)s\n' % res.headers)
        sys.stdout.write('URL: {}\n'.format(self.url))
        sys.stdout.write('Concurrency level: {}\n'.format(self.concurrency))
        sys.stdout.write('Options: {}\n\n'.format(self.options))

    @property
    def run(self):
        try:
            self.method = getattr(requests, self.method.lower())

            start = time.time()
            sys.stdout.flush()
            sys.stdout.write('[')

            pool = Pool(self.concurrency)

            if self.duration:
                with gevent.Timeout(self.duration, False):
                    while True:
                        pool.spawn(call, self.method, self.url, self.options)
                    pool.join()
            else:
                for number in xrange(self.numbers):
                    pool.spawn(call, self.method, self.url, self.options)
                pool.join()

            self.time_process = time.time() - start
            sys.stdout.flush()
            sys.stdout.write(']')
        except Exception as error:
            sys.stdout.write('error during run process ({})\n'.format(error))
            exit(1)

    @property
    def stats(self):
        try:
            self.total = sum([len(_stats[key]) for key in _stats.iterkeys()])
            self.total_success = len(_stats[200])
            if self.total_success:
                self.min = min(_stats[200])
                self.max = max(_stats[200])
                self.moy = sum(_stats[200]) / self.total_success
            else:
                self.min = 0
                self.max = 0
                self.moy = 0
            self.total_failed = self.total - self.total_success
            self.RPS = self.total_success / self.time_process
        except Exception as error:
            sys.stdout.write('error during stats process ({})\n'.format(error))
            pass

    @property
    def output(self):
        sys.stdout.write('\nNumber process requests: {}\n'.format(self.total))
        sys.stdout.write('Time taken for tests: {:.2f}\n\n'.format(self.time_process))
        sys.stdout.write('Complete requests: {}\n'.format(self.total_success))
        sys.stdout.write('Failed requests: {}\n\n'.format(self.total_failed))
        sys.stdout.write('Faster request: {:.3f}\n'.format(self.min))
        sys.stdout.write('Slower request: {:.3f}\n'.format(self.max))
        sys.stdout.write('Time per request (only success): {:.3f}\n'.format(self.moy))
        sys.stdout.write('Request per second: {:.2f}\n'.format(self.RPS))


def main():
    # parser
    parser = argparse.ArgumentParser(description='Overload tools')
    parser.add_argument('url', metavar='url', type=str, help='URL you want overload')
    parser.add_argument('--method', dest='method', default='GET', type=str, choices=HTTP_VERBS, help='HTTP method.')
    parser.add_argument('--concurrency', dest='concurrency', default=1, type=int, help='Number of multiple requests to perform at a time. Default is one request at a time.')
    parser.add_argument('--numbers', dest='numbers', default=1, type=int, help='Number of requests to perform for the benchmarking session. Default is one request.')
    parser.add_argument('--cookies', dest='cookies', nargs='*', default=[], type=str, help='Send your own cookies. cookie:value')
    parser.add_argument('--content-type', dest='ct', default=[], type=str, help='Specify our content-type.')
    parser.add_argument('--timeout', dest='timeout', default=None, type=float, help='You can tell requests to stop waiting for a response after a given number of seconds.')
    parser.add_argument('--auth', dest='auth', default=None, type=str, help='Making requests with HTTP Basic Auth. user:password')
    parser.add_argument('--duration', dest='duration', default=None, type=int, help='Duration. Override the --numbers option.')
    parser.add_argument('--repeat', dest='repeat', default=1, type=int, help='Repeat the benchmark.')
    parser.add_argument('--quiet', dest='quiet', action='store_true', help='The general outcome is hidden.')
    args = parser.parse_args()

    # arguments
    url = args.url
    method = args.method
    concurrency = args.concurrency
    numbers = args.numbers
    cookies = args.cookies
    ct = args.ct
    timeout = args.timeout
    auth = args.auth
    duration = args.duration
    repeat = args.repeat
    quiet = args.quiet
    options = {}

    if not method in HTTP_VERBS:
        sys.stdout.write('discarding unknown method: {}\n\n'.format(method))
        parser.print_usage()
        exit(1)

    if cookies:
        options['cookies'] = cookies_parse(cookies)

    if ct:
        options['headers'] = {'content-type': ct}

    if timeout:
        options['timeout'] = timeout

    if auth:
        auth = tuple(auth.split(':', 1))
        if len(auth) != 2:
            sys.stdout.write('discardind invalid auth: {}\n\n'.format(auth))
            parser.print_usage()
            exit(1)
        else:
            options['auth'] = auth

    if quiet:
        null = open(os.devnull, 'wb')
        sys.stdout = null

    # app
    try:
        _loop = 1
        for loop in xrange(repeat):
            overload = Overload(url, method, concurrency, numbers, duration, **options)
            overload.informations
            overload.run
            overload.stats
            overload.output
            if _loop != repeat:
                clear_stats()
                _loop += 1
                sys.stdout.write('\nwait 3 seconds...\n\n')
                gevent.sleep(3)
    except KeyboardInterrupt:
        pass
    except Exception as error:
        sys.stdout.write('error during app process ({})\n'.format(error))
        exit(1)
    else:
        exit(0)

if __name__ == '__main__':
    main()
