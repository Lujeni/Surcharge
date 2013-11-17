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

# not re-implemented yet
# missing options: repeat, duration, CT, overflow

# [--data=<data>]
# [--cookie=<cookie>]
# [--timeout=<seconds>]

# -d --data=<data>                    Send data [default: {}].
# -C --cookie=<cookie>                Adds cookies [default: {}].
# -t --timeout=<seconds>              You can tell requests to stop waiting for a response after a given number of seconds [default: 0].
# -a --auth=<auth>                    BasicAuthentication [default: {}].

from process import Surcharger

from docopt import docopt, DocoptExit
# mhhhh: ugly import
from __init__ import __version__

if __name__ == '__main__':

    try:
        arguments = docopt(__doc__, version=__version__)
        url = arguments.pop('<url>')
        method = arguments.pop('--method')
        concurrency = int(arguments.pop('--concurrency'))
        numbers = int(arguments.pop('--numbers'))
    except Exception:
        print DocoptExit()
    else:
        s = Surcharger(
            url=url,
            method=method,
            concurrency=concurrency,
            numbers=numbers,
            **arguments
        )
        s()
