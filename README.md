Overload - *in progress*
=======================

Overload is a tool for benchmarking your web server like apache benchmark.

For a memory efficiency, *Overload* uses the gevent networking library.

Usage
=====
```bash
usage: overload.py [-h] [-m METHOD] [-c CONCURRENCY] [-n NUMBERS]
                   [--cookies [COOKIES [COOKIES ...]]]
                   url

Overload benchmark

positional arguments:
  url                   URL you want overload

optional arguments:
  -h, --help            show this help message and exit
  -m METHOD             HTTP method. Default it's Get
  -c CONCURRENCY        Number of multiple requests to perform at a time.
                        Default is one request at a time.
  -n NUMBERS            Number of requests to perform for the benchmarking
                        session. Default is one request.
  --cookies [COOKIES [COOKIES ...]]
                        Send your own cookies: firstcookie:value,
                        secondcookie:value
```

Example
=======
```bash
# simple call
$ python overload.py -n 10 -c 5 http://google.com

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
$ python overload.py http://httpbin.org/cookies --cookies 'ck:1', 'cook:value'

[-]

Concurrency level: 1
Number process requests: 1
Time taken for tests: 0.57

Complete requests: 1
Failed requests: 0

Faster request: 0.566
Slower request: 0.566
Time per request (only success): 0.566
```
