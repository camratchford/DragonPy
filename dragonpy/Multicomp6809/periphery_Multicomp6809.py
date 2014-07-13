#!/usr/bin/env python
# encoding:utf8

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================


    http://searle.hostei.com/grant/Multicomp/


    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import logging
import sys
import os

try:
    import Tkinter
except Exception, err:
    print "Error importing Tkinter: %s" % err
    Tkinter = None


from dragonpy.components.periphery import PeripheryBase, TkPeripheryBase


log = logging.getLogger("DragonPy.Multicomp6809.Periphery")


class Multicomp6809PeripheryBase(PeripheryBase):
    def __init__(self, cfg):
        super(Multicomp6809PeripheryBase, self).__init__(cfg)

#     BUS_ADDR_AREAS = (
#         (0xFFD8, 0xFFDF, "SD Card"),
#         (0xFFD2, 0xFFD3, "Interface 2"),
#         (0xFFD0, 0xFFD1, "Interface 1 (serial interface or TV/Keyboard)"),
#         (0xBFF0, 0xBFFF, "Interrupt vectors"),
#     )

        self.read_address2func_map = {
            0xFFD0: self.read_acia_status, # Control/status port of ACIA
            0xFFD1: self.read_acia_data, # Data port of ACIA
            0xbffe: self.reset_vector,
        }
        self.write_address2func_map = {
            0xFFD0: self.write_acia_status, # Control/status port of ACIA
            0xFFD1: self.write_acia_data, # Data port of ACIA
        }

    def reset_vector(self, cpu_cycles, op_address, address):
        return self.cfg.ROM_START + 0x0046

    def write_acia_status(self, cpu_cycles, op_address, address, value):
        return 0xff
    def read_acia_status(self, cpu_cycles, op_address, address):
        return 0x03

    def read_acia_data(self, cpu_cycles, op_address, address):
        if self.user_input_queue.empty():
            return 0x0

        char = self.user_input_queue.get()
        value = ord(char)
        log.error("%04x| (%i) read from ACIA-data, send back %r $%x",
            op_address, cpu_cycles, char, value
        )
        return value

    def write_acia_data(self, cpu_cycles, op_address, address, value):
        char = chr(value)
#        log.error("*"*79)
#        log.error("Write to screen: %s ($%x)" , repr(char), value)
#        log.error("*"*79)

        if value >= 0x90: # FIXME: Why?
            value -= 0x60
            char = chr(value)
#            log.error("convert value -= 0x30 to %s ($%x)" , repr(char), value)

        if value <= 9: # FIXME: Why?
            value += 0x41
            char = chr(value)
#            log.error("convert value += 0x41 to %s ($%x)" , repr(char), value)

        self.output_queue.put(char)




class Multicomp6809PeripheryTk(TkPeripheryBase, Multicomp6809PeripheryBase):
    TITLE = "DragonPy - Multicomp 6809"
    GEOMETRY = "+500+300"
    INITAL_INPUT = "\r\n".join([
#         'PRINT "HELLO WORLD!"',
#         '? 123',

        '10 FOR I=1 TO 3',
        '20 PRINT STR$(I)+" DRAGONPY"',
        '30 NEXT I',
        'RUN',
        '',
        'LIST',
    ]) + "\r\n"

    def event_return(self, event):
        self.user_input_queue.put("\r")
#         self.user_input_queue.put("\n")

    _STOP_AFTER_OK_COUNT = None
#     _STOP_AFTER_OK_COUNT = 2
    def update(self, cpu_cycles):
        is_empty = self.output_queue.empty()
        super(Multicomp6809PeripheryTk, self).update(cpu_cycles)
        if self._STOP_AFTER_OK_COUNT is not None and not is_empty:
            txt = self.text.get(1.0, Tkinter.END)
            if txt.count("OK\r\n") >= self._STOP_AFTER_OK_COUNT:
                log.error("-> exit!")
                self.destroy()


# Multicomp6809Periphery = Multicomp6809PeripherySerial
Multicomp6809Periphery = Multicomp6809PeripheryTk


def test_run():
    import subprocess
    cmd_args = [
        sys.executable,
#         "/usr/bin/pypy",
        os.path.join("..", "DragonPy_CLI.py"),
#         "--verbosity=5",
#         "--verbosity=10", # DEBUG
#         "--verbosity=20", # INFO
#         "--verbosity=30", # WARNING
#         "--verbosity=40", # ERROR
        "--verbosity=50", # CRITICAL/FATAL

#                       "--max=1660000",
#         "--max=1000",

        "--cfg=Multicomp6809",
    ]
    print "Startup CLI with: %s" % " ".join(cmd_args[1:])
    subprocess.Popen(cmd_args, cwd="..").wait()

if __name__ == "__main__":
    test_run()
