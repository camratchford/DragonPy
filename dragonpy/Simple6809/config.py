# coding: utf-8

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================

    :created: 2013-2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2013-2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import os

from dragonpy.core.configs import BaseConfig
from dragonpy.Simple6809.mem_info import get_simple6809_meminfo
from dragonpy.Simple6809.periphery_simple6809 import Simple6809Periphery


class Simple6809Cfg(BaseConfig):
    """
    DragonPy config for Grant Searle's Simple 6809 design
    More info read ./Simple6809/README.creole
    """
    RAM_START = 0x0000
    RAM_END = 0x03FF # 1KB
    # RAM_END = 0x07FF # 2KB
    # RAM_END = 0x0FFF # 4KB
#     RAM_END = 0x1FFF # 8KB
    # RAM_END = 0x3FFF # 16KB
    # RAM_END = 0x7FFF # 32KB

    ROM_START = 0xC000
    ROM_END = 0xFFFF
    ROM_SIZE = 0x4000 # 16384 Bytes

    RESET_VECTOR = 0xBFFE
    RESET_VECTOR_VALUE = 0xdb46 # ROM_START + 0x1b46

    BUS_ADDR_AREAS = (
        (0xa000, 0xbfef, "RS232 interface"),
        (0xbff0, 0xbfff, "Interrupt vectors"),
    )

    # Used in unittest for init the BASIC Interpreter:
    STARTUP_END_ADDR = 0xdf2b # == JSR  LA390          GO GET AN INPUT LINE

    DEFAULT_ROM = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "ExBasROM.bin"
    )

    def __init__(self, cfg_dict):
        self.ROM_SIZE = (self.ROM_END - self.ROM_START) + 1
        self.RAM_SIZE = (self.RAM_END - self.RAM_START) + 1
        super(Simple6809Cfg, self).__init__(cfg_dict)

#         if self.verbosity <= logging.INFO:
        self.mem_info = get_simple6809_meminfo()

        self.periphery_class = Simple6809Periphery

        self.memory_callbacks = {
#            (0x004f, 0x0054): (None, self.float_accu_write0),
#            (0x005c, 0x0061): (None, self.float_accu_write1),
        }

    def float_accu_write0(self, cpu, addr, value):
        print "%04x| Write float accu 0 $%x to $%x %s" % (
            cpu.last_op_address, value, addr,
            self.mem_info.get_shortest(addr)
        )
        cpu.memory.ram.print_dump(0x004f, 0x0054)

    def float_accu_write1(self, cpu, addr, value):
        print "%04x| Write float accu 1 $%x to $%x %s" % (
            cpu.last_op_address, value, addr,
            self.mem_info.get_shortest(addr)
        )
        cpu.memory.ram.print_dump(0x005c, 0x0061)

config = Simple6809Cfg

def test_run():
    import sys, subprocess
    cmd_args = [sys.executable,
        os.path.join("..", "DragonPy_CLI.py"),
#        "--verbosity=5",
#         "--verbosity=10", # DEBUG
#         "--verbosity=20", # INFO
#        "--verbosity=30", # WARNING
#         "--verbosity=40", # ERROR
        "--verbosity=50", # CRITICAL/FATAL

        "--cfg=Simple6809",
#         "--max=500000",
#         "--max=20000",
        "--max=1",
    ]
    print "Startup CLI with: %s" % " ".join(cmd_args[1:])
    subprocess.Popen(cmd_args, cwd="..").wait()

if __name__ == "__main__":
    test_run()
