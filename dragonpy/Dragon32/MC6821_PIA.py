#!/usr/bin/env python
# encoding:utf8

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================

    http://www.6809.org.uk/dragon/hardware.shtml#pia0

    :created: 2013 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2013-2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.

    Based on: XRoar emulator by Ciaran Anscomb (GPL license) more info, see README
"""

from dragonpy.utils.logging_utils import log
import Queue
from dragonpy.Dragon32.keyboard_map import get_dragon_col_row_values


class PIA_register(object):
    def __init__(self, name):
        self.name = name
        self.reset()

    def reset(self):
        self.control_register = 0x0
        self.direction_register = 0x0
        self.output_register = 0x0
        self.interrupt_received = 0x0
        self.irq = 0x0


class PIA(object):
    """
    PIA - MC6821 - Peripheral Interface Adaptor
    """
    def __init__(self, cfg):
        self.cfg = cfg
        self.pia_0_A_registers = PIA_register("PIA0 A")
        self.pia_0_B_registers = PIA_register("PIA0 B")
        self.pia_1_A_registers = PIA_register("PIA1 A")
        self.pia_1_B_registers = PIA_register("PIA1 B")

        self.keyboard_col = 0xff
        self.keyboard_row = 0xff
        self.keyboard_col_send = True
        self.keyboard_row_send = True

    def get_write_func_map(self):
        #
        # TODO: Collect this information via a decorator simmilar to op codes in CPU!
        #
        write_func_map = {
            0xff00: self.write_PIA0_A_data, #    PIA 0 A side Data reg.
            0xff01: self.write_PIA0_A_control, # PIA 0 A side Control reg.
            0xff02: self.write_PIA0_B_data, #    PIA 0 B side Data reg.
            0xff03: self.write_PIA0_B_control, # PIA 0 B side Control reg.

            0xff06: self.write_serial_interface, # Only Dragon 64

            0xff20: self.write_PIA1_A_data, #    PIA 1 A side Data reg.
            0xff21: self.write_PIA1_A_control, # PIA 1 A side Control reg.
            0xff22: self.write_PIA1_B_data, #    PIA 1 B side Data reg.
            0xff23: self.write_PIA1_B_control, # PIA 1 B side Control reg.
        }
        return write_func_map

    def get_read_func_map(self):
        read_func_map = {
            0xff00: self.read_PIA0_A_data, #    PIA 0 A side Data reg.
            0xff01: self.read_PIA0_A_control, # PIA 0 A side Control reg.
            0xff02: self.read_PIA0_B_data, #    PIA 0 B side Data reg.
            0xff03: self.read_PIA0_B_control, # PIA 0 B side Control reg.

            0xff04: self.read_serial_interface, # Only Dragon 64

            0xff20: self.read_PIA1_A_data, #    PIA 1 A side Data reg.
            0xff21: self.read_PIA1_A_control, # PIA 1 A side Control reg.
            0xff22: self.read_PIA1_B_data, #    PIA 1 B side Data reg.
            0xff23: self.read_PIA1_B_control, # PIA 1 B side Control reg.
        }
        return read_func_map

    def reset(self):
        self.pia_0_A_registers.reset()
        self.pia_0_B_registers.reset()
        self.pia_1_A_registers.reset()
        self.pia_1_B_registers.reset()

    #--------------------------------------------------------------------------

    def key_down(self, value):
        log.critical("Add user key down %r %r to PIA input queue.", repr(value), chr(value))
        col, row = get_dragon_col_row_values(value)
        self.keyboard_col = col #& self.keyboard_col
        self.keyboard_row = row #& self.keyboard_row
        self.keyboard_col_send = False
        self.keyboard_row_send = False
        log.critical("Set col: $%02x - row: $%02x", self.keyboard_col, self.keyboard_row)

    #--------------------------------------------------------------------------

    def read_PIA0_A_data(self, cpu_cycles, op_address, address):
        """ read from 0xff00 -> PIA 0 A side Data reg. """
        log.error("TODO: read from 0xff00 -> PIA 0 A side Data reg.")
        return 0x00

    def read_PIA0_A_control(self, cpu_cycles, op_address, address):
        """ read from 0xff01 -> PIA 0 A side Control reg. """
        log.error("TODO: read from 0xff01 -> PIA 0 A side Control reg.")
        return 0xb3

    def read_PIA1_A_data(self, cpu_cycles, op_address, address):
        """ read from 0xff20 -> PIA 1 A side Data reg. """
        log.error("TODO: read from 0xff20 -> PIA 1 A side Data reg.")
        return 0x01

    def read_PIA1_A_control(self, cpu_cycles, op_address, address):
        """ read from 0xff21 -> PIA 1 A side Control reg. """
        log.error("TODO: read from 0xff21 -> PIA 1 A side Control reg.")
        return 0x34

    def read_PIA1_B_data(self, cpu_cycles, op_address, address):
        """ read from 0xff22 -> PIA 1 B side Data reg. """
        log.error("TODO: read from 0xff22 -> PIA 1 B side Data reg.")
        return 0x00

    def read_PIA1_B_control(self, cpu_cycles, op_address, address):
        """ read from 0xff23 -> PIA 1 B side Control reg. """
        log.error("TODO: read from 0xff23 -> PIA 1 B side Control reg.")
        return 0x37

    #--------------------------------------------------------------------------

    def write_PIA0_A_data(self, cpu_cycles, op_address, address, value):
        """ write to 0xff00 -> PIA 0 A side Data reg. """
        log.error("TODO: write $%02x to 0xff00 -> PIA 0 A side Data reg.", value)

    def write_PIA0_A_control(self, cpu_cycles, op_address, address, value):
        """ write to 0xff01 -> PIA 0 A side Control reg. """
        log.error("TODO: write $%02x to 0xff01 -> PIA 0 A side Control reg.", value)

    def write_PIA1_A_data(self, cpu_cycles, op_address, address, value):
        """ write to 0xff20 -> PIA 1 A side Data reg. """
        log.error("TODO: write $%02x to 0xff20 -> PIA 1 A side Data reg.", value)

    def write_PIA1_A_control(self, cpu_cycles, op_address, address, value):
        """ write to 0xff21 -> PIA 1 A side Control reg. """
        log.error("TODO: write $%02x to 0xff21 -> PIA 1 A side Control reg.", value)

    def write_PIA1_B_data(self, cpu_cycles, op_address, address, value):
        """ write to 0xff22 -> PIA 1 B side Data reg. """
        log.error("TODO: write $%02x to 0xff22 -> PIA 1 B side Data reg.", value)

    def write_PIA1_B_control(self, cpu_cycles, op_address, address, value):
        """ write to 0xff23 -> PIA 1 B side Control reg. """
        log.error("TODO: write $%02x to 0xff23 -> PIA 1 B side Control reg.", value)

    #--------------------------------------------------------------------------

    def read_serial_interface(self, cpu_cycles, op_address, address):
        log.error("TODO: read from $%04x (D64 serial interface", address)
        return 0x00

    def write_serial_interface(self, cpu_cycles, op_address, address, value):
        log.error("TODO: write $%02x to $%04x (D64 serial interface", value, address)

    #--------------------------------------------------------------------------
    # Keyboard

    def read_PIA0_B_data(self, cpu_cycles, op_address, address):
        """ read from 0xff02 -> PIA 0 B side Data reg. """
        self.keyboard_col_send = True
        result = self.keyboard_col
        #self.keyboard_col = 0xff
        log.critical(
            "%04x| read $%04x (PIA 0 B side Data reg.) send $%02x back.",
            op_address, address, result
        )
        return result

    def read_PIA0_B_control(self, cpu_cycles, op_address, address):
        """ read from 0xff03 -> PIA 0 B side Control reg. """
        self.keyboard_row_send = True
        result = self.keyboard_row
        #self.keyboard_row = 0xff
        log.critical(
            "%04x| read $%04x (PIA 0 B side Control reg.) send $%02x back.",
            op_address, address, result
        )
        return result

    def write_PIA0_B_data(self, cpu_cycles, op_address, address, value):
        """ write to 0xff02 -> PIA 0 B side Data reg. """
        log.critical("%04x| write $%02x to 0xff02 -> PIA 0 B side Data reg.", op_address, value)
        if self.keyboard_col_send:
#            self.keyboard_col = value
#            self.keyboard_col &= value
#            self.keyboard_col &= ~value
            self.keyboard_col = ~value & 0xff

    def write_PIA0_B_control(self, cpu_cycles, op_address, address, value):
        """ write to 0xff03 -> PIA 0 B side Control reg. """
        log.critical("%04x| write $%02x to 0xff03 -> PIA 0 B side Control reg.", op_address, value)
        if self.keyboard_row_send:
#            self.keyboard_row = value
#            self.keyboard_row &= value
#            self.keyboard_row &= ~value
            self.keyboard_row = ~value & 0xff



def test_run():
    import sys, os, subprocess
    cmd_args = [
        sys.executable,
        os.path.join("..", "Dragon64_test.py"),
    ]
    print "Startup CLI with: %s" % " ".join(cmd_args[1:])
    subprocess.Popen(cmd_args, cwd="..").wait()

if __name__ == "__main__":
    test_run()
