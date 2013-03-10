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
