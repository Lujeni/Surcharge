#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from zmq import Context
from zmq import SUB, PUB, REP, REQ
from zmq import SUBSCRIBE

from random import randint
from json import dumps
from json import loads


class Master(object):

    def __init__(self, number_workers):
        self.context = Context()
        self.number_workers = number_workers
        self.workers = set()

    @property
    def init_pubsocket(self):
        self.pubsocket = self.context.socket(PUB)
        self.pubsocket.bind('tcp://*:6666')

    @property
    def init_repsocket(self):
        self.repsocket = self.context.socket(REP)
        self.repsocket.bind('tcp://*:7777')

    @property
    def wait_workers(self):
        while len(self.workers) != self.number_workers:
            # an worker is ready
            message = loads(self.repsocket.recv_json())
            self.workers.add(message['_id'])
            self.repsocket.send('ok')
            sys.stdout.write('worker {} is ready\n'.format(message['_id']))

    @property
    def launch_benchmark(self):
        self.pubsocket.send('OVERFLOW')


class Worker(object):

    def __init__(self):
        self.context = Context()
        self.worker_id = randint(1, 100000)

    @property
    def init_subsocket(self):
        self.subsocket = self.context.socket(SUB)
        self.subsocket.connect('tcp://localhost:6666')
        self.subsocket.setsockopt(SUBSCRIBE, '')

    @property
    def init_reqsocket(self):
        self.reqsocket = self.context.socket(REQ)
        self.reqsocket.connect('tcp://localhost:7777')

    @property
    def iam_ready(self):
        ready = False
        while not ready:
            msg = {'_id': self.worker_id}
            self.reqsocket.send_json(dumps(msg))
            if self.reqsocket.recv() == 'ok':
                ready = True

    @property
    def waiting_benchmark(self):
        while True:
            self.subsocket.recv()
            break
