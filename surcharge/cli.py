# -*- coding: utf-8 -*-

"""
Usage:
    surcharge <url>
        [--method=<method>]
        [--concurrency=<clients>]
        [--numbers=<requests>]

Options:
    -h --help                           Show this screen.
    -v --version                        Show version.
    -m --method=<method>                HTTP method [default: GET].
    -c --concurrency=<clients>          Number of multiple requests to perform at a time [default: 1].
    -n --numbers=<requests>             Number of requests to perform for the benchmarking session [default: 1].

"""


from surcharge import __version__
from surcharge.core import Surcharger, SurchargerStats
from surcharge.libs.docopt import docopt, DocoptExit


def main():
    try:
        arguments = docopt(__doc__, version=__version__)
        url = arguments.pop('<url>')
        method = arguments.pop('--method')
        concurrency = int(arguments.pop('--concurrency'))
        numbers = int(arguments.pop('--numbers'))
    except Exception:
        print DocoptExit()
    else:
        surcharger = Surcharger(
            url=url,
            method=method,
            concurrency=concurrency,
            numbers=numbers,
            cli=True,
            **arguments
        )
        surcharger()

        stats = SurchargerStats(surcharger=surcharger)
        stats()

if __name__ == '__main__':
    main()
