# -*- coding: utf-8 -*-

__version__ = '0.9.0'
__name__ = 'surcharge'
__author__ = 'Lujeni'


from logging import getLogger, INFO, Formatter
from logging.handlers import RotatingFileHandler


logger = getLogger()
logger.setLevel(INFO)
formatter = Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

file_handler = RotatingFileHandler('/tmp/surcharge_activity.log', 'a', 1000000, 1)
file_handler.setLevel(INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
