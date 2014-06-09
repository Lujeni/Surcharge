# -*- coding: utf-8 -*-

"""
Usage:
    surcharge <url>
        [--method=<method>]
        [--concurrency=<clients>]
        [--numbers=<requests> | --duration=<seconds]

Options:
    -h --help                           Show this screen.
    -v --version                        Show version.
    -m --method=<method>                HTTP method [default: GET].
    -c --concurrency=<clients>          Number of multiple requests to perform at a time [default: 1].
    -n --numbers=<requests>             Number of requests to perform for the benchmarking session [default: 1].
    -D --duration=<seconds>             Duration in seconds. Override the --numbers option [default: 0]

"""

import sys

from surcharge import __version__, logger
from surcharge.core import Surcharger, SurchargerStats
from surcharge.libs.docopt import docopt, DocoptExit


def main():
    try:
        arguments = docopt(__doc__, version=__version__)
        surcharger_args = {
            'url': arguments.pop('<url>'),
            'method': arguments.pop('--method'),
            'concurrency': int(arguments.pop('--concurrency')),
            'numbers': int(arguments.pop('--numbers')),
            'duration': int(arguments.pop('--duration')),
            'cli': True,
        }
    except Exception as e:
        mess = "cli error :: {}".format(e)
        logger.info(mess)
        sys.stdout(mess)
        sys.stdout(DocoptExit())
    else:
        surcharger = Surcharger(**surcharger_args)
        surcharger()

        stats = SurchargerStats(surcharger=surcharger)
        stats()

if __name__ == '__main__':
    main()
