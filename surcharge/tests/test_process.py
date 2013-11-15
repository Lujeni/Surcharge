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
    Exceptions = namedtuple('Exceptions', 'MissingOption BadOption MissingResult')
    from _exceptions import MissingOption, BadOption, MissingResult
    return Exceptions(MissingOption, BadOption, MissingResult)


@pytest.fixture
def surcharger():
    from process import Surcharger
    return Surcharger(url='http://google.com')


def test_url(surcharger, exceptions):
    """
    Test the URL parameter
    """

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
    """
    Test the METHOD parameter
    """

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


def test_format(surcharger, exceptions):
    """
    Test the FORMAT parameter
    """

    # generic test
    assert hasattr(surcharger, 'format')
    assert hasattr(surcharger, '_format')
    assert isinstance(surcharger.format, unicode)
    assert getattr(surcharger._format, 'name')
    assert getattr(surcharger._format, 'function')
    assert surcharger.format == u'json'

    #
    surcharger.format = 'xml'
    assert surcharger.format == u'xml'

    # exceptions
    with pytest.raises(exceptions.MissingOption):
        surcharger.format = None
        surcharger.format = ''

    with pytest.raises(exceptions.BadOption):
        surcharger.format = 'yaml'


def test_surcharge(surcharger):
    """
    Test the SURCHARGE method
    """

    # generic test
    surcharger()
    assert surcharger.result
    assert len(surcharger.result) == 1

    result = surcharger.result[0]
    assert hasattr(result, 'status_code')
    assert hasattr(result, 'exec_time')
    assert isinstance(result.status_code, int)
    assert isinstance(result.exec_time, float)

    #
    surcharger.numbers = 10
    surcharger()
    assert surcharger.result
    assert len(surcharger.result) == 10
    for res in surcharger.result:
        assert hasattr(res, 'status_code')
        assert hasattr(result, 'exec_time')
        assert isinstance(res.status_code, int)
        assert isinstance(res.exec_time, float)


def test_retrieve_result(surcharger, exceptions):
    """
    Test the RETRIEVE_RESULT method
    """

    # generic test (json format)
    surcharger()
    res = surcharger.retrieve_result()
    assert isinstance(res, list)
    for r in res:
        assert isinstance(r, dict)
        assert 'status_code' in r
        assert 'exec_time' in r

    # default format
    surcharger.format = 'default'
    res = surcharger.retrieve_result()
    assert isinstance(res, list)
    for r in res:
        assert hasattr(r, 'status_code')
        assert hasattr(r, 'exec_time')

    # exceptions
    with pytest.raises(NotImplementedError):
        surcharger.format = 'xml'
        surcharger.retrieve_result()

    with pytest.raises(exceptions.MissingResult):
        surcharger.result = []
        surcharger.retrieve_result()


