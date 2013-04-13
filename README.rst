Surcharge
=========

**Surcharge** is a tool for benchmarking your web server like **apache benchmark**.

Surcharge uses the **gevent** networking library. Using the **greenlets** allow to spawn many concurrent requests with little memory.

HTTP requests are made with **requests** library.

**Overflow** is a module of Surcharge. It's allows to launch several benchmarks dynamically through the network. Overflow uses the **zeroMQ** library. (overflow is not available with the version on pypi)

Example
=======
::


  # simple call
  $ python surcharge.py --numbers 10 --concurrency 5 --url http://google.com

  Server: gws
  URL: http://google.com
  Concurrency level: 5
  Options: {}

  [----------]

  Number process requests: 10
  Time taken for tests: 5.91

  Complete requests: 10
  Failed requests: 0

  Faster request: 0.464
  Slower request: 5.443
  Time per request (only success): 1.226
  Request per second: 0.82

  # call with multiple cookies
  $ python surcharge.py --url http://httpbin.org/cookies --cookies ck:1, cook:value

  # call with HTTP Basic Auth
  $ python surcharge.py --url https://secure.test.com --auth user:password

  # bench during 10 seconds
  $ python surcharge.py --url http://google.com --concurrency 10 --duration 10

  # repeat the same bench twice
  $ python surcharge.py --url http://google.com --concurrency 10 --duration 10 --repeat 2

Overflow Example
================
::


  # launch overflow master. Listen to specified IP and to specified port
  $ python surcharge.py --master *:7777

  # populate multiple workers
  $ python surcharge.py --url http://google.fr --worker localhost:7777 --duration 10 --concurrency 10
  $ python surcharge.py --url http://google.com --worker localhost:7777 --numbers 100 --concurrency 20
  $ python surcharge.py --url http://www.google.co.uk --worker localhost:7777

  # starts the benchmark across all workers
  $ python surcharge.py --launcher localhost:7777


Install
=======
::


  $ pip install surcharge #and enjoy

Usage
=====
::


  usage: surcharge.py [-h] [--url URL] [--method {GET,POST,PUT,DELETE}]
                      [--concurrency CONCURRENCY] [--numbers NUMBERS]
                      [--cookies [COOKIES [COOKIES ...]]] [--content-type CT]
                      [--timeout TIMEOUT] [--auth AUTH] [--duration DURATION]
                      [--repeat REPEAT] [--quiet] [--master MASTER]
                      [--worker WORKER] [--launcher LAUNCHER]

  Surcharge tools

  optional arguments:
    -h, --help            show this help message and exit
    --url URL, -U URL     URL you want overload
    --method {GET,POST,PUT,DELETE}, -m {GET,POST,PUT,DELETE}
                          HTTP method.
    --concurrency CONCURRENCY, -c CONCURRENCY
                          Number of multiple requests to perform at a time.
                          Default is one request at a time.
    --numbers NUMBERS, -n NUMBERS
                          Number of requests to perform for the benchmarking
                          session. Default is one request.
    --cookies [COOKIES [COOKIES ...]], -C [COOKIES [COOKIES ...]]
                          Send your own cookies. cookie:value
    --content-type CT, -ct CT
                          Specify our content-type.
    --timeout TIMEOUT, -T TIMEOUT
                          You can tell requests to stop waiting for a response
                          after a given number of seconds.
    --auth AUTH, -A AUTH  Making requests with HTTP Basic Auth. user:password
    --duration DURATION, -D DURATION
                          Duration. Override the --numbers option.
    --repeat REPEAT, -R REPEAT
                          Repeat the benchmark.
    --quiet, -q           The general outcome is hidden.
    --master MASTER       Overflow master.
    --worker WORKER       Overflow worker
    --launcher LAUNCHER   Overflow launcher
