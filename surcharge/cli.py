# -*- coding: utf-8 -*-

"""
Usage:
    surcharge <url>
        [--method=<method>]
        [--concurrency=<clients>]
        [--numbers=<requests> | --duration=<seconds>]
        [--timeout=<seconds>]
        [--cookies=<cookies>]
        [--auth=<credentials>]
        [--quiet]

Options:
    -h --help                           Show this screen.
    -v --version                        Show version.
    -m --method=<method>                HTTP method [default: GET].
    -c --concurrency=<clients>          Number of multiple requests to perform at a time [default: 1].
    -n --numbers=<requests>             Number of requests to perform for the benchmarking session [default: 1].
    -D --duration=<seconds>             Duration in seconds. Override the --numbers option [default: 0]
    -T --timeout=<seconds>              You can tell requests to stop waiting for a response after a given number of seconds [default: 2].
    -C --cookies=<cookies>              Send your own cookies. [default: {}]
    -A --auth=<credentials>             Making requests with HTTP Basic Auth. [default: None]
    -Q --quiet                          Disable the default stdout
"""

from ast import literal_eval

from surcharge import __version__, logger
from surcharge.core import Surcharger, SurchargerStats
from surcharge.libs.docopt import docopt, DocoptExit


def main():
    try:
        arguments = docopt(__doc__, version=__version__)
        quiet = arguments.pop('--quiet')
        surcharger_args = {
            'url': arguments.pop('<url>'),
            'method': arguments.pop('--method'),
            'concurrency': int(arguments.pop('--concurrency')),
            'numbers': int(arguments.pop('--numbers')),
            'duration': int(arguments.pop('--duration')),
            'cli': False if quiet else True,
            'timeout': float(arguments.pop('--timeout')),
            'cookies': literal_eval(arguments.pop('--cookies'))
        }

        auth = arguments.pop('--auth')
        if auth:
            surcharger_args['auth'] = tuple(auth.split(':'))

    except Exception as e:
        mess = "cli error :: {}".format(e)
        logger.info(mess)
        print "{}\n".format(mess)
        print DocoptExit()
    else:
        surcharger = Surcharger(**surcharger_args)
        surcharger()

        stats = SurchargerStats(surcharger=surcharger)
        stats()

if __name__ == '__main__':
    main()
