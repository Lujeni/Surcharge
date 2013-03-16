#/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import sys
import shlex
import unittest
import gevent
import surcharge as S

from gevent.pywsgi import WSGIServer


cmd = shlex.split("%s -c 'from tests import run; run()'" % sys.executable)
server = None


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return ['<b>Hello world!</b>\n']


def run():
    WSGIServer(('localhost', 8080), application).serve_forever()


def start_server():
    global server
    server = subprocess.Popen(cmd)


def stop_server():
    global server
    server.terminate()
    server = None


class TestSurcharge(unittest.TestCase):

    def setUp(self):
        start_server()
        gevent.sleep(1)
        url = 'http://localhost:8080'
        method = 'GET'
        concurrency = 1
        self.numbers = 10
        duration = None
        options = {}
        self.surcharge = S.Surcharge(url, method, concurrency, self.numbers, duration, **options)

    def test_simple_call(self):
        self.surcharge.run
        self.surcharge.stats
        self.assertEquals(self.surcharge.total_success, self.numbers)

    def tearDown(self):
        gevent.sleep(5)
        stop_server()

if __name__ == '__main__':
    unittest.main()
