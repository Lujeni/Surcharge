Overload - *in progress*
=======================

Overload is a tool for benchmarking your web server like apache benchmark.

For a memory efficiency, *Overload* uses the gevent networking library.

Usage
=====
```bash
usage: overload.py [-h] [-method -m {GET,POST,PUT,DELETE}]
                   [--concurrency -c CONCURRENCY] [--numbers -n NUMBERS]
                   [--cookies -ck [COOKIES [COOKIES ...]]]
                   [--content-type -ct CT] [--timeout -t TIMEOUT]
                   [--auth -a AUTH]
                   url

Overload tools

positional arguments:
  url                   URL you want overload

optional arguments:
  -h, --help            show this help message and exit
  -method -m {GET,POST,PUT,DELETE}
                        HTTP method.
  --concurrency -c CONCURRENCY
                        Number of multiple requests to perform at a time.
                        Default is one request at a time.
  --numbers -n NUMBERS  Number of requests to perform for the benchmarking
                        session. Default is one request.
  --cookies -ck [COOKIES [COOKIES ...]]
                        Send your own cookies. cookie:value
  --content-type -ct CT
                        Specify our content-type.
  --timeout -t TIMEOUT  You can tell requests to stop waiting for a response
                        after a given number of seconds.
  --auth -a AUTH        Making requests with HTTP Basic Auth. user:password
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
$ python overload.py http://httpbin.org/cookies --cookies ck:1, cook:value

# call with HTTP Basic Auth
$ python overload.py https://secure.test.com --auth user:password

```
