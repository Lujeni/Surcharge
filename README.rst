===================================
Surcharge - refactoring in progress
===================================
.. image:: https://pypip.in/d/surcharge/badge.png
        :target: https://crate.io/packages/surcharge/

Introduction
============
**Surcharge** is a tool for benchmarking your web server like **apache benchmark**.
Surcharge uses the **gevent** networking library. Using the **greenlets** allow to spawn many concurrent requests with little memory.
HTTP requests are made with **requests** library.


Requirements
============
This code has been run on Python 2.7
::

  requests==1.2.0
  gevent==0.13.7

Installation
============
::

  $ pip install surcharge #and enjoy

Tests
=====

Example command
===============
::


  # simple call
  $ surcharge http://google.com --numbers 10 --concurrency 5

  # standard stdout
  Server: gws

  URL: http://173.194.67.138:80

  Concurrency level: 5

  Options: {'cookies': {}, 'timeout': 2.0}


  100% |############################|


  Number process requests: 10
  Time taken for tests: 0.57
  Complete requests: 10
  Failed requests: 0
  Faster request: 0.045
  Slower request: 0.059
  Time per request (only success): 0.051
  Request per second: 98.57

  # call with multiple cookies
  $ surcharge http://httpbin.org/cookies --cookies "{'ck':1, 'cook':value}"

  # call with HTTP Basic Auth
  $ surcharge https://secure.test.com --auth "('user', 'password')"

  # bench during 10 seconds
  $ surcharge http://google.com --concurrency 10 --duration 10


Example API
===========
::


  # see the constructor or the surcharge/cli.py for more details
  >>> from surcharge.core import Surcharger
  >>> surcharge = Surcharger(url='http://google.com')
  >>> surcharge()

  >>> surcharge.result
  defaultdict(<type 'list'>, {200: [0.06690406799316406]})

  # compute simple stat
  >>> from surcharge.core import SurchargerStats
  >>> surcharge_stats = SurchargerStats(surcharge)
  >>> surcharge_stats()

  >>> surcharge_stats.stats
  {'RPS': 14.20353538774128,
 'exec_time': 0.07088184356689453,
 'max': 0.0704050064086914,
 'min': 0.0704050064086914,
 'moy': 0.0704050064086914,
 'requests_process': 0.0704050064086914,
 'total': 1,
 'total_failed': 0,
 'total_success': 1}

  # By default, stdout is used to display the stats
  # You can override the SurchargerStats.send method and make what you want with the stats

Usage
=====
::


  Usage:
      surcharge <url>
          [--method=<method>]
          [--concurrency=<clients>]
          [--numbers=<requests> | --duration=<seconds>]
          [--timeout=<seconds>]
          [--cookies=<cookies>]

  Options:
      -h --help                           Show this screen.
      -v --version                        Show version.
      -m --method=<method>                HTTP method [default: GET].
      -c --concurrency=<clients>          Number of multiple requests to perform at a time [default: 1].
      -n --numbers=<requests>             Number of requests to perform for the benchmarking session [default: 1].
      -D --duration=<seconds>             Duration in seconds. Override the --numbers option [default: 0]
      -T --timeout=<seconds>              You can tell requests to stop waiting for a response after a given number of seconds [default: 2].
      -C --cookies=<cookies>              Send your own cookies. [default: {}]


Deprecated - need refactoring
=============================
 (`since 0.8`) **Overflow** is a module of Surcharge. It's allows to launch several benchmarks dynamically through the network. Overflow uses the **zeroMQ** library.

License
=======
This project is lecensed under the MIT license, a copy of which can be found in the LICENSE file.

