Overload - *in progress*
=======================

Overload is a tool for benchmarking your web server like apache benchmark.

For a memory efficiency, *Overload* uses the gevent networking library.

Usage
=====
```bash
usage: overload.py [-h] [-m METHOD] [-c CONCURRENCY] [-n NUMBERS]
                   url [url ...]

Overload benchmark

positional arguments:
  url             URL you want overload

optional arguments:
  -h, --help      show this help message and exit
  -m METHOD       HTTP method
  -c CONCURRENCY  Number of multiple requests to perform at a time. Default is
                  one request at a time
  -n NUMBERS      Number of requests to perform for the benchmarking session.
                  The default is to just perform a single request which
                  usually leads to non-representative benchmarking results
```

Example
=======
```bash
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
```
