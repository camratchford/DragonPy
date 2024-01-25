#!/usr/bin/env python

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================


    :created: 2013-2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2013-2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import logging
import queue
import sys
from typing import Callable

from dragonpy.components.periphery import ConsolePeripheryMixin
from dragonpy.mx6309.peripherals import DEFAULT_PERIPHERALS


log = logging.getLogger(__name__)


# todo: Why?
try:
    import tkinter
except ImportError:
    log.critical("Error importing Tkinter!")
    tkinter = None


class MX6309Periphery:
    TITLE = "MX6309 Test program"
    peripherals: list = DEFAULT_PERIPHERALS

    def __init__(self, cfg, cpu, memory, display_callback: Callable, user_input_queue: queue.Queue):
        self.cfg = cfg
        self.cpu = cpu
        self.memory = memory
        self.display_callback = display_callback
        self.user_input_queue = user_input_queue

        self.peripherals = [peripheral(self) for peripheral in self.peripherals]


class MX6309PeripheryConsole(MX6309Periphery, ConsolePeripheryMixin):
    """
    A simple console to interact with the 6809 simulation.
    """

    def new_output_char(self, char):
        sys.stdout.write(char)
        sys.stdout.flush()



