#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
import logging
from handler import SinklogHandler


USAGE = """
    example usage:

    # log a message on the command line
    $ sinklog -k <logkey> "my log message"

    # log from stdin
    $ tail -f /var/log/myapp.log | sinklog -k <logkey>
"""

LEVELS = {
    'ERROR': logging.ERROR,
    'WARN': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}


def main():
    parser = argparse.ArgumentParser(
        "sinklog", formatter_class=argparse.RawDescriptionHelpFormatter,
        description="a simple logger for sinklog.com", epilog=USAGE)
    parser.add_argument(
        "--key", "-k", required=True, help="sinklog.com log key")
    parser.add_argument(
        "--host", "-H", default=SinklogHandler.DEFAULT_HOST, help="syslog host")
    parser.add_argument(
        "--port", "-P", default=SinklogHandler.DEFAULT_PORT, type=int, help="syslog port")
    parser.add_argument(
        "--format", "-F", default="%(message)s", help="Python log format")
    parser.add_argument(
        "--level", "-l", default="INFO", choices=LEVELS.keys(), help="Python log level")
    parser.add_argument(
        "--tee", "-t", action="store_true",
        help="when reading from stdin also write input to stdout")
    parser.add_argument(
        "message", nargs="?", help="messages to log")
    args = parser.parse_args()

    logger = logging.getLogger("sinklog")
    level = LEVELS[args.level]
    logger.setLevel(level)
    handler = SinklogHandler(logkey=args.key, address=(args.host, args.port))
    handler.setFormatter(logging.Formatter(args.format))
    logger.addHandler(handler)

    def log(msg):
        logger.log(level, msg)
        if args.tee:
            sys.stdout.write(msg)

    if args.message:
        log(args.message)
    else:
        for line in sys.stdin:
            log(line)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
