Overload - *in progress*
=======================

Overload is a tool for benchmarking your web server like apache benchmark.

For a memory efficiency, *Overload* uses the gevent networking library.

Usage
=====
```bash
usage: overload.py [-h] [-method {GET,POST,PUT,DELETE}]
                   [--concurrency CONCURRENCY] [--numbers NUMBERS]
                   [--cookies [COOKIES [COOKIES ...]]] [--content-type CT]
                   [--timeout TIMEOUT] [--auth AUTH] [--duration DURATION]
                   url

Overload tools

positional arguments:
  url                   URL you want overload

optional arguments:
  -h, --help            show this help message and exit
  -method {GET,POST,PUT,DELETE}
                        HTTP method.
  --concurrency CONCURRENCY
                        Number of multiple requests to perform at a time.
                        Default is one request at a time.
  --numbers NUMBERS     Number of requests to perform for the benchmarking
                        session. Default is one request.
  --cookies [COOKIES [COOKIES ...]]
                        Send your own cookies. cookie:value
  --content-type CT     Specify our content-type.
  --timeout TIMEOUT     You can tell requests to stop waiting for a response
                        after a given number of seconds.
  --auth AUTH           Making requests with HTTP Basic Auth. user:password
  --duration DURATION   Duration. Override the --numbers option.
  --repeat REPEAT       Repeat the benchmark.
```

Example
=======
```bash
# simple call
$ python overload.py --numbers 10 --concurrency 5 http://google.com

[----------]

Concurrency level: 5
Number process requests: 10
Time taken for tests: 5.15

Complete requests: 10
Failed requests: 0

Faster request: 0.511
Slower request: 4.113
Time per request (only success): 1.942

# call with multiple cookies
$ python overload.py http://httpbin.org/cookies --cookies ck:1, cook:value

# call with HTTP Basic Auth
$ python overload.py https://secure.test.com --auth user:password

# bench during 10 seconds
$ python overload.py http://google.com --concurrency 10 --duration 10

# repeat the same bench twice
$ python overload.py http://google.com --concurrency 10 --duration 10 --repeat 2
```
