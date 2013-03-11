#/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

import time
import requests
import argparse

from gevent.pool import Pool
from collections import defaultdict
from sys import exit
from sys import stdout


_methods = 'GET', 'POST'
_stats = defaultdict(list)


def progress(func):
    def wrapper(*args):
        stdout.write('-')
        stdout.flush()
        return func(*args)
    return wrapper


# TODO: fix bug AttributeError: 'Greenlet' object has no attribute '_run'
@progress
def call(method, url):
    try:
        start = time.time()
        res = method(url)
        code = res.status_code
    except Exception as error:
        code = 404
    finally:
        _stats[code].append(time.time()-start)


class Overload(object):

    def __init__(self, url, method='GET', concurrency=1, numbers=1, **options):
        self.url = url
        self.method = method
        self.concurrency = concurrency
        self.numbers = numbers
        self.options = options

    @property
    def run(self):
        try:
            self.method = getattr(requests, self.method.lower())
            start = time.time()
            stdout.flush()
            stdout.write('[')
            pool = Pool(self.concurrency)
            for number in xrange(self.numbers):
                pool.spawn(call, self.method, self.url)
            pool.join()
            self.time_process = time.time() - start
            stdout.flush()
            stdout.write(']')
        except Exception as error:
            stdout.write('error during run process ({})'.format(error))
            exit(1)

    @property
    def stats(self):
        self.total = sum([len(_stats[key]) for key in _stats.iterkeys()])
        self.total_success = len(_stats[200])
        self.min = min(_stats[200])
        self.max = max(_stats[200])
        self.moy = sum(_stats[200]) / self.total_success

    @property
    def output(self):
        stdout.write('\nConcurrency level: {}\n'.format(self.concurrency))
        stdout.write('Number process requests: {}\n'.format(self.total))
        stdout.write('Time taken for tests: {:.2f}\n\n'.format(self.time_process))
        stdout.write('Complete requests: {}\n'.format(self.total_success))
        stdout.write('Failed requests: {}\n\n'.format(self.total-self.total_success))
        stdout.write('Faster request: {:.3f}\n'.format(self.min))
        stdout.write('Slower request: {:.3f}\n'.format(self.max))
        stdout.write('Time per request (only success): {:.3f}\n'.format(self.moy))


def main():
    # parser
    parser = argparse.ArgumentParser(description='Overload benchmark')
    parser.add_argument('url', metavar='url', type=str, nargs='+', help='URL you want overload')
    parser.add_argument('-m', dest='method', default='GET', type=str, help='HTTP method')
    parser.add_argument('-c', dest='concurrency', default=1, type=int, help='Number of multiple requests to perform at a time. Default is one request at a time')
    parser.add_argument('-n', dest='numbers', default=1, type=int, help='''Number of requests to perform for the benchmarking session. The default is to just perform a single request which usually leads to non-representative benchmarking results''')
    args = parser.parse_args()

    # arguments
    url = args.url[0]
    method = args.method
    concurrency = args.concurrency
    numbers = args.numbers

    # app
    try:
        overload = Overload(url, method=method, concurrency=concurrency, numbers=numbers)
        overload.run
        overload.stats
        overload.output
    except KeyboardInterrupt:
        pass
    finally:
        exit(0)

if __name__ == '__main__':
    main()
