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


def test_url_property(surcharger, exceptions):

    # generic test
    assert hasattr(surcharger, 'url')
    assert hasattr(surcharger, '_url')
    assert isinstance(surcharger.url, unicode)
    assert getattr(surcharger._url, 'fqn')
    assert getattr(surcharger._url, 'resolv')
    assert surcharger.url == u'http://google.com'
    assert 'http' in surcharger._url.resolv
    assert len(surcharger._url.resolv.split(':')) == 3

    # localhost test
    surcharger.url = 'http://localhost'
    url_test = urlparse(surcharger._url.resolv)

    assert url_test.scheme == 'http'
    assert url_test.netloc == '127.0.0.1:80'

    # exceptions
    with pytest.raises(exceptions.MissingOption):
        surcharger.url = None
        surcharger.url = ''
