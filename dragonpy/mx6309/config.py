"""
    DragonPy - Dragon 32 emulator in Python
    =======================================

    :created: 2013 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2013-2015 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


from dragonlib.api import CoCoAPI

from dragonpy import constants
from dragonpy.core.configs import BaseConfig
from dragonpy.mx6309.mem_info import get_mx6309_meminfo
from dragonpy.mx6309.periphery import MX6309Periphery
from dragonpy.mx6309.rom import MX6309Rom

from dragonpy.mx6309 import constants


class MX6309Config(BaseConfig):
    """
    DragonPy config for Lennart's 6809 single board computer

        Buggy machine language monitor and rudimentary O.S. version 1.0

    More info read ./mx6309/README.creole
    """

    CONFIG_NAME = constants.MX6309
    MACHINE_NAME = "Cam's Modular 6309-based computer"

    RAM_START = 0x0000
    RAM_END = 0x7FFF
    # RAM size: 0x8000 == 32768 Bytes

    ROM_START = 0x8000
    ROM_END = 0xFFFF
    # ROM size: 0x4000 == 16384 Bytes

    BUS_ADDR_AREAS = (
        (0xe000, 0xe001, "RS232 interface"),  # emulated serial port (ACIA)
        (0xFFF2, 0xFFFE, "Interrupt vectors"),
    )

    DEFAULT_ROMS = (
        MX6309Rom(address=0xC000, max_size=2**13),
    )

    # Used in unittest for init the machine:
    STARTUP_END_ADDR = 0xe45a  # == O.S. routine to read a character into B register.

    def __init__(self, cmd_args):
        super().__init__(cmd_args)

        self.machine_api = CoCoAPI()  # FIXME!

#         if self.verbosity <= logging.INFO:
        self.mem_info = get_mx6309_meminfo()

        self.periphery_class = MX6309Periphery


config = MX6309Config
