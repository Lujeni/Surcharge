#/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
import argparse

from gevent.pool import Pool
from collections import defaultdict
from sys import exit
from sys import stdout


_stats = defaultdict(list)
_methods = 'GET', 'POST'
_protocols = ['HTTP', 'HTTPS']


def _call(url, method, **options):
    start = time.time()
    res = method(url, **options)
    _stats[res.status_code].append(start-time.time())


def _run(url, method='GET', concurrency=1, numbers=1, **options):

    protocol = url.split(':')[0].upper()

    if not protocol in _protocols:
        stdout.write('discarding invalid url: {}\n'.format(url))
        exit(1)

    if not method.upper() in _methods:
        stdout.write('unknown method: {}\n'.format(method))
        exit(1)
    else:
        method = getattr(requests, method.lower())

    if numbers:
        stdout.write("spawn {} workers\n".format(concurrency))
        stdout.write("process {} requests\n".format(numbers))
        pool = Pool(concurrency)
        for number in xrange(numbers):
            pool.spawn(_call, url, method, **options)
        pool.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Overload benchmark')

    parser.add_argument('url', metavar='url', type=str, nargs='+', help='URL you want overload')
    parser.add_argument('-n', dest='numbers', type=int, help='''Number of requests to perform for the benchmarking session. The default is to just perform a single request which usually leads to non-representative benchmarking results''')
    args = parser.parse_args()

    url = args.url[0]
    numbers = 1 if not args.numbers else args.numbers

    _run(url, numbers=numbers)

    stdout.write("{}\n".format(_stats))
