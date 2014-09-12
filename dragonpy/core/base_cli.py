#!/usr/bin/env python2
# coding: utf-8

"""
    base commandline interface
    ==========================

    :created: 2013 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2013-2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function


import argparse
import sys
import logging

log = logging.getLogger(__name__)


def get_log_levels():
    levels = [100, 99] # FIXME
    try:
        # Python 3
        levels += logging._nameToLevel.values()
    except AttributeError:
        # Python 2
        levels += [level for level in logging._levelNames if isinstance(level, int)]

    levels.sort()
    return levels

LOG_LEVELS = get_log_levels()


class ActionLogList(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print("A list of all loggers:")
        for log_name in sorted(logging.Logger.manager.loggerDict):
            print("\t%s" % log_name)
        parser.exit()


class Base_CLI(object):
    DESCRIPTION = None
    EPOLOG = None
    VERSION = None
#     DEFAULT_LOG_FORMATTER = "%(message)s"
#     DEFAULT_LOG_FORMATTER = "%(processName)s/%(threadName)s %(message)s"
#     DEFAULT_LOG_FORMATTER = "[%(processName)s %(threadName)s] %(message)s"
#     DEFAULT_LOG_FORMATTER = "[%(levelname)s %(asctime)s %(module)s] %(message)s"
    DEFAULT_LOG_FORMATTER = "%(levelname)8s %(created)f %(module)s] %(message)s"

    def __init__(self):
        self.logfilename = None

        arg_kwargs = {}
        if self.DESCRIPTION is not None:
            arg_kwargs["description"] = self.DESCRIPTION
        if self.EPOLOG is not None:
            arg_kwargs["epilog"] = self.EPOLOG

        self.parser = argparse.ArgumentParser(**arg_kwargs)

        if self.VERSION is not None:
            self.parser.add_argument('--version', action='version',
                version='%%(prog)s %s' % self.VERSION
            )

        self.parser.add_argument("--log",
            nargs="*",
            help="Setup loggers, e.g.: --log DragonPy.cpu6809,50 dragonpy.Dragon32.MC6821_PIA,10"
        )

        self.parser.register('action', "log_list", ActionLogList)
        self.parser.add_argument("-l", "--log_list",
            action="log_list", nargs=0,
            help="List all exiting loggers and exit."
        )

        self.parser.add_argument("--verbosity",
            type=int, choices=LOG_LEVELS, default=logging.CRITICAL,
            help=(
                "verbosity level to stdout (lower == more output!)"
                " (default: %s)" % logging.INFO
            )
        )
        self.parser.add_argument("--log_formatter",
            default=self.DEFAULT_LOG_FORMATTER,
            help=(
                "see: http://docs.python.org/2/library/logging.html#logrecord-attributes"
            )
        )

    def parse_args(self, args=None):
        if self.DESCRIPTION is not None:
            print()
            print(self.DESCRIPTION, self.VERSION)
            print("-"*79)
            print()

        args = self.parser.parse_args(args)

#         for arg, value in sorted(vars(args).items()):
#             log.debug("argument %s: %r", arg, value)
#             print "argument %s: %r" % (arg, value)

        return args

    def setup_logging(self, args):
        if args.log is None:
            return

        print(args.log)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(args.log_formatter)
        handler.setFormatter(formatter)

        for logger_cfg in args.log:
            logger_name, level = logger_cfg.rsplit(",", 1)
            level = int(level)
            logger = logging.getLogger(logger_name)
            logger.handlers = (handler,)

            logger.setLevel(logging.INFO)
            logger.info("Set %i level to logger %r", level, logger_name)
            logger.setLevel(level)


#------------------------------------------------------------------------------


def test_run():
    import os
    import subprocess
    cmd_args = [
        sys.executable,
        os.path.join("..", "DragonPy_CLI.py"),
#         "--version",
#         "-h"
#         "--log_list",
        "--verbosity", "50",
        "--log",
            "DragonPy.cpu6809,10",
            "dragonpy.Dragon32.MC6821_PIA,99",
            "dragonpy.Dragon32.MC6883_SAM,40",

#         "--verbosity", " 1", # hardcode DEBUG ;)
#         "--verbosity", "10", # DEBUG
#         "--verbosity", "20", # INFO
#         "--verbosity", "30", # WARNING
#         "--verbosity", "40", # ERROR
#         "--verbosity", "50", # CRITICAL/FATAL
#         "--verbosity", "99", # nearly all off
        "--machine", "Dragon32", "run",
#        "--machine", "Vectrex", "run",
#        "--max_ops", "1",
#        "--trace",
    ]
    print("Startup CLI with: %s" % " ".join(cmd_args[1:]))
    subprocess.Popen(cmd_args, cwd="..").wait()


if __name__ == "__main__":
    import doctest
    print(doctest.testmod(
        verbose=False
        # verbose=True
    ))

#     cli = Base_CLI()
#     cli.parse_args(args=["--help"])
#     cli.parse_args(args=["--log_list"])

    test_run()
