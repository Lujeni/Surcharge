# -*- coding: utf-8 -*-

# PTH import
from os import path
from site import addsitedir
CUR_DIR = path.dirname(path.realpath(__file__))
addsitedir(CUR_DIR)

from collections import namedtuple
from urlparse import urlparse

import pytest


@pytest.fixture
def exceptions():
    Exceptions = namedtuple('Exceptions', 'MissingOption BadOption')
    from process import MissingOption, BadOption
    return Exceptions(MissingOption, BadOption)


@pytest.fixture
def surcharger():
    from process import Surcharger
    return Surcharger(url='http://google.com')


def test_url(surcharger, exceptions):

    # generic test
    assert hasattr(surcharger, 'url')
    assert hasattr(surcharger, '_url')
    assert isinstance(surcharger.url, unicode)
    assert getattr(surcharger._url, 'fqn')
    assert getattr(surcharger._url, 'addr')
    assert surcharger.url == u'http://google.com'

    # localhost test
    surcharger.url = 'http://localhost'
    url_test = urlparse(surcharger._url.addr)
    assert url_test.scheme == 'http'
    assert url_test.netloc == '127.0.0.1:80'

    surcharger.url = 'https://localhost:8080'
    url_test = urlparse(surcharger._url.addr)
    assert url_test.scheme == 'https'
    assert url_test.netloc == '127.0.0.1:8080'

    # exceptions
    with pytest.raises(exceptions.MissingOption):
        surcharger.url = None
        surcharger.url = ''

    with pytest.raises(exceptions.BadOption):
        surcharger.url = 'localhost'
        surcharger.url = 'http//localhost'


def test_method(surcharger, exceptions):

    # generic test
    assert hasattr(surcharger, 'method')
    assert hasattr(surcharger, '_method')
    assert isinstance(surcharger.method, unicode)
    assert getattr(surcharger._method, 'name')
    assert getattr(surcharger._method, 'function')
    assert surcharger.method == u'GET'

    #
    surcharger.method = 'post'
    assert surcharger.method == u'POST'

    # exceptions
    with pytest.raises(exceptions.MissingOption):
        surcharger.method = None
        surcharger.method = ''

    with pytest.raises(exceptions.BadOption):
        surcharger.method = 'PUT'
